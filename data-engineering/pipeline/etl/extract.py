from typing import Generator, Optional
import time
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from pipeline.utils.logging import get_logger
from config import settings

logger = get_logger("extract")

BASE_QUERY = """
    SELECT cr.id, cr.dataset_id, cr.rule_id, cr.passed,
           cr.failed_rows, cr.total_rows, cr.checked_at,
           vr.name AS rule_name, vr.rule_type, vr.severity,
           vr.field_name, vr.dataset_type, vr.is_active,
           d.name AS dataset_name, d.file_type,
           d.row_count AS dataset_row_count, d.column_count,
           d.uploaded_at, d.status AS dataset_status
    FROM check_results cr
    JOIN validation_rules vr ON cr.rule_id = vr.id
    JOIN datasets d ON cr.dataset_id = d.id
"""

INCREMENTAL_FILTER = " WHERE cr.checked_at > :last_run"


class ExtractionError(Exception):
    pass


def _build_query(mode: str, last_run) -> tuple[str, dict]:
    if mode == "incremental" and last_run:
        return BASE_QUERY + INCREMENTAL_FILTER, {"last_run": last_run}
    return BASE_QUERY, {}


def _retry_operation(func, max_attempts: int, delay: float):
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except OperationalError as e:
            last_error = e
            if attempt < max_attempts:
                logger.warning("Attempt %d failed, retrying in %.1fs: %s", attempt, delay, e)
                time.sleep(delay)
            else:
                logger.error("All %d attempts failed", max_attempts)
    raise ExtractionError(f"Extraction failed after {max_attempts} attempts: {last_error}") from last_error


def extract(engine: Engine, mode: str = "full", last_run=None) -> pd.DataFrame:
    """Full extraction - loads all records into memory. Use extract_chunked() for large datasets."""
    retry_attempts = settings["etl"].get("retry_attempts", 3)
    retry_delay = settings["etl"].get("retry_delay_seconds", 5)
    
    logger.info("Extracting all data into memory - Mode: %s", mode)
    
    query_str, params = _build_query(mode, last_run)
    
    def do_extract():
        with engine.connect() as conn:
            return pd.read_sql(text(query_str), conn, params=params)
    
    try:
        df = _retry_operation(do_extract, retry_attempts, retry_delay)
        logger.info("Extracted %d records (full load)", len(df))
        return df
        
    except SQLAlchemyError as e:
        logger.error("Query execution failed: %s", e)
        raise ExtractionError(f"Extraction query failed: {e}") from e


def extract_chunked(
    engine: Engine,
    mode: str = "full",
    last_run=None,
    chunk_size: Optional[int] = None
) -> Generator[pd.DataFrame, None, None]:
    """Chunked extraction - yields DataFrames in batches for memory efficiency."""
    chunk_size = chunk_size or settings["etl"]["batch_size"]
    retry_attempts = settings["etl"].get("retry_attempts", 3)
    retry_delay = settings["etl"].get("retry_delay_seconds", 5)
    
    expected_count = get_record_count(engine, mode, last_run)
    expected_chunks = (expected_count + chunk_size - 1) // chunk_size if expected_count > 0 else 0
    logger.info("Starting chunked extraction - ~%d records in ~%d chunks of %d", expected_count, expected_chunks, chunk_size)
    
    query_str, params = _build_query(mode, last_run)
    
    def get_chunks():
        with engine.connect() as conn:
            return pd.read_sql(
                text(query_str),
                conn,
                params=params,
                chunksize=chunk_size
            )
    
    try:
        chunk_iter = _retry_operation(get_chunks, retry_attempts, retry_delay)
        
        total_records = 0
        chunk_num = 0
        for chunk in chunk_iter:
            chunk_num += 1
            total_records += len(chunk)
            logger.info("Yielding chunk %d (%d records, %d total)", chunk_num, len(chunk), total_records)
            yield chunk
            
        logger.info("Chunked extraction complete - %d chunks, %d total records", chunk_num, total_records)
        
    except SQLAlchemyError as e:
        logger.error("Chunked extraction failed: %s", e)
        raise ExtractionError(f"Chunked extraction failed: {e}") from e


def get_record_count(engine: Engine, mode: str = "full", last_run=None) -> int:
    """Get record count directly from check_results table (avoids heavy join)."""
    if mode == "incremental" and last_run:
        count_query = "SELECT COUNT(*) FROM check_results WHERE checked_at > :last_run"
        params = {"last_run": last_run}
    else:
        count_query = "SELECT COUNT(*) FROM check_results"
        params = {}
    
    with engine.connect() as conn:
        return conn.execute(text(count_query), params).scalar() or 0
