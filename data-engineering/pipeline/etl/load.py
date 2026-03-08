from dataclasses import dataclass
from typing import Optional
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection, Engine

from pipeline.utils.logging import get_logger
from infrastructure.db import AnalyticsBase
from infrastructure import models  # noqa: F401
from config import settings

logger = get_logger("load")

BATCH_SIZE = settings["etl"]["batch_size"]


@dataclass
class LoadSummary:
    dim_datasets: int = 0
    dim_rules: int = 0
    dim_date: int = 0
    fact_quality_checks: int = 0
    
    def to_dict(self) -> dict:
        return {
            "dim_datasets": self.dim_datasets,
            "dim_rules": self.dim_rules,
            "dim_date": self.dim_date,
            "fact_quality_checks": self.fact_quality_checks,
        }


@dataclass
class UpsertConfig:
    table: str
    columns: list[str]
    conflict_column: str
    update_on_conflict: bool = True


UPSERT_CONFIGS = {
    "dim_datasets": UpsertConfig(
        table="dim_datasets",
        columns=["id", "name", "file_type", "row_count", "column_count", "status", "uploaded_at"],
        conflict_column="id",
        update_on_conflict=True,
    ),
    "dim_rules": UpsertConfig(
        table="dim_rules",
        columns=["id", "name", "field_name", "rule_type", "severity", "dataset_type", "is_active"],
        conflict_column="id",
        update_on_conflict=True,
    ),
    "dim_date": UpsertConfig(
        table="dim_date",
        columns=["date_key", "full_date", "day_of_week", "month", "quarter", "year"],
        conflict_column="date_key",
        update_on_conflict=False,
    ),
}


def _to_native(row: dict) -> dict:
    result = {}
    for k, v in row.items():
        if hasattr(v, "item"):
            result[k] = v.item()
        elif isinstance(v, pd.Timestamp):
            result[k] = v.to_pydatetime()
        else:
            result[k] = v
    return result


def _validate_dataframe(df: pd.DataFrame, name: str) -> bool:
    if df is None or df.empty:
        logger.warning("Empty DataFrame for %s - skipping", name)
        return False
    return True


def _build_upsert_sql(config: UpsertConfig, is_sqlite: bool) -> str:
    columns_str = ", ".join(config.columns)
    placeholders = ", ".join(f":{col}" for col in config.columns)
    
    if is_sqlite:
        if config.update_on_conflict:
            return f"INSERT OR REPLACE INTO {config.table} ({columns_str}) VALUES ({placeholders})"
        return f"INSERT OR IGNORE INTO {config.table} ({columns_str}) VALUES ({placeholders})"
    
    if config.update_on_conflict:
        update_cols = [c for c in config.columns if c != config.conflict_column]
        update_str = ", ".join(f"{c} = EXCLUDED.{c}" for c in update_cols)
        return f"""
            INSERT INTO {config.table} ({columns_str}) VALUES ({placeholders})
            ON CONFLICT ({config.conflict_column}) DO UPDATE SET {update_str}
        """
    return f"""
        INSERT INTO {config.table} ({columns_str}) VALUES ({placeholders})
        ON CONFLICT ({config.conflict_column}) DO NOTHING
    """


def _upsert_dimension(conn: Connection, df: pd.DataFrame, config: UpsertConfig, is_sqlite: bool) -> int:
    if not _validate_dataframe(df, config.table):
        return 0
    
    sql = _build_upsert_sql(config, is_sqlite)
    stmt = text(sql)
    
    rows = [_to_native(row) for row in df.to_dict(orient="records")]
    
    for row in rows:
        conn.execute(stmt, row)
    
    logger.info("Upserted %d rows into %s", len(rows), config.table)
    return len(rows)


def _insert_facts_batched(conn: Connection, df: pd.DataFrame) -> int:
    if not _validate_dataframe(df, "fact_quality_checks"):
        return 0
    
    stmt = text("""
        INSERT INTO fact_quality_checks 
        (dataset_id, rule_id, date_key, passed, failed_rows, total_rows, score, checked_at)
        VALUES (:dataset_id, :rule_id, :date_key, :passed, :failed_rows, :total_rows, :score, :checked_at)
    """)
    
    rows = [_to_native(row) for row in df.to_dict(orient="records")]
    total = len(rows)
    batch_count = 0
    
    for i in range(0, total, BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        for row in batch:
            conn.execute(stmt, row)
        batch_count += 1
        
        if batch_count % 10 == 0 or i + BATCH_SIZE >= total:
            logger.info("Inserted fact batch %d (%d/%d records)", batch_count, min(i + BATCH_SIZE, total), total)
    
    logger.info("Inserted %d fact rows in %d batches", total, batch_count)
    return total


def load(engine: Engine, transformed_data: Optional[dict]) -> dict:
    if transformed_data is None:
        logger.warning("No transformed data to load")
        return LoadSummary().to_dict()
    
    AnalyticsBase.metadata.create_all(engine)
    is_sqlite = "sqlite" in engine.dialect.name
    
    summary = LoadSummary()
    
    with engine.begin() as conn:
        summary.dim_datasets = _upsert_dimension(
            conn, transformed_data.get("dim_datasets"), UPSERT_CONFIGS["dim_datasets"], is_sqlite
        )
        summary.dim_rules = _upsert_dimension(
            conn, transformed_data.get("dim_rules"), UPSERT_CONFIGS["dim_rules"], is_sqlite
        )
        summary.dim_date = _upsert_dimension(
            conn, transformed_data.get("dim_date"), UPSERT_CONFIGS["dim_date"], is_sqlite
        )
        summary.fact_quality_checks = _insert_facts_batched(
            conn, transformed_data.get("facts")
        )
    
    logger.info("Load complete - %s", summary.to_dict())
    return summary.to_dict()
