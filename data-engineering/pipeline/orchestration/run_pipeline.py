from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import json
import uuid
import pandas as pd

from infrastructure.db import get_source_engine, get_target_engine
from pipeline.utils.logging import get_logger
from pipeline.etl.extract import extract_chunked, ExtractionError
from pipeline.etl.transform import transform, ValidationError
from pipeline.etl.load import load
from pipeline.etl.validate import validate, validation_passed

logger = get_logger("pipeline")

STATE_FILE = Path(__file__).parent.parent.parent / "logs" / "pipeline_state.json"


@dataclass
class PipelineMetrics:
    records_extracted: int = 0
    records_transformed: int = 0
    records_loaded: int = 0
    dimensions_loaded: dict = field(default_factory=dict)
    extraction_duration: Optional[timedelta] = None
    transform_duration: Optional[timedelta] = None
    load_duration: Optional[timedelta] = None
    validate_duration: Optional[timedelta] = None


@dataclass
class PipelineResult:
    success: bool = False
    run_id: str = ""
    mode: str = "full"
    dry_run: bool = False
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[timedelta] = None
    metrics: PipelineMetrics = field(default_factory=PipelineMetrics)
    warnings: list[str] = field(default_factory=list)
    error: Optional[str] = None
    validation_passed: bool = True
    
    def to_dict(self) -> dict:
        result = asdict(self)
        result["start_time"] = self.start_time.isoformat() if self.start_time else None
        result["end_time"] = self.end_time.isoformat() if self.end_time else None
        result["duration"] = str(self.duration) if self.duration else None
        result["metrics"]["extraction_duration"] = str(self.metrics.extraction_duration) if self.metrics.extraction_duration else None
        result["metrics"]["transform_duration"] = str(self.metrics.transform_duration) if self.metrics.transform_duration else None
        result["metrics"]["load_duration"] = str(self.metrics.load_duration) if self.metrics.load_duration else None
        result["metrics"]["validate_duration"] = str(self.metrics.validate_duration) if self.metrics.validate_duration else None
        return result
    
    @property
    def summary(self) -> dict:
        return self.metrics.dimensions_loaded


def _load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def _save_state(state: dict):
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


def run(mode: str = "full", dry_run: bool = False) -> PipelineResult:
    run_id = str(uuid.uuid4())[:8]
    start = datetime.now()
    
    result = PipelineResult(
        run_id=run_id,
        mode=mode,
        dry_run=dry_run,
        start_time=start,
        metrics=PipelineMetrics(),
    )
    
    logger.info("=" * 60)
    logger.info("ETL pipeline started - Run: %s, Mode: %s, Dry run: %s", run_id, mode, dry_run)
    logger.info("=" * 60)

    try:
        source = get_source_engine()
        target = get_target_engine()

        state = _load_state()
        last_run = state.get("last_successful_run") if mode == "incremental" else None

        step_start = datetime.now()
        logger.info("Step 1/4: Extract (chunked)")
        chunks = list(extract_chunked(source, mode=mode, last_run=last_run))
        result.metrics.extraction_duration = datetime.now() - step_start
        
        if not chunks:
            logger.warning("No data extracted - pipeline stopping")
            result.success = True
            result.warnings.append("No data to process")
            return result
        
        raw = pd.concat(chunks, ignore_index=True)
        result.metrics.records_extracted = len(raw)

        step_start = datetime.now()
        logger.info("Step 2/4: Transform")
        transformed = transform(raw)
        result.metrics.transform_duration = datetime.now() - step_start
        
        if transformed:
            result.metrics.records_transformed = len(transformed.get("facts", []))

        if dry_run:
            logger.info("Dry run - skipping load and validate")
            result.success = True
            result.metrics.dimensions_loaded = {"dry_run": True}
            return result

        step_start = datetime.now()
        logger.info("Step 3/4: Load")
        summary = load(target, transformed)
        result.metrics.load_duration = datetime.now() - step_start
        result.metrics.dimensions_loaded = summary
        result.metrics.records_loaded = summary.get("fact_quality_checks", 0)

        step_start = datetime.now()
        logger.info("Step 4/4: Validate")
        warnings = validate(source, target)
        result.metrics.validate_duration = datetime.now() - step_start
        result.warnings = [str(w) for w in warnings]
        result.validation_passed = validation_passed(warnings)

        if result.validation_passed:
            state["last_successful_run"] = start.isoformat()
            state["last_run_id"] = run_id
            _save_state(state)
            logger.info("State saved - last successful run: %s", start.isoformat())
        else:
            logger.warning("Validation failed - state NOT saved")

        result.success = True

    except ExtractionError as e:
        logger.error("Pipeline failed during extraction: %s", e)
        result.error = f"Extraction failed: {e}"
        result.warnings.append(result.error)

    except ValidationError as e:
        logger.error("Pipeline failed during transform: %s", e)
        result.error = f"Validation failed: {e}"
        result.warnings.append(result.error)

    except Exception as e:
        logger.exception("Pipeline failed with unexpected error")
        result.error = f"Unexpected error: {e}"
        result.warnings.append(result.error)

    finally:
        end = datetime.now()
        result.end_time = end
        result.duration = end - start
        
        logger.info("=" * 60)
        logger.info("Pipeline finished - Run: %s", run_id)
        logger.info("Duration: %s", result.duration)
        logger.info("Success: %s | Validation: %s", result.success, "PASSED" if result.validation_passed else "FAILED")
        logger.info("Metrics: extracted=%d, transformed=%d, loaded=%d",
                    result.metrics.records_extracted,
                    result.metrics.records_transformed,
                    result.metrics.records_loaded)
        logger.info("=" * 60)

    return result


if __name__ == "__main__":
    run()
