from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from sqlalchemy import text
from sqlalchemy.engine import Engine

from pipeline.utils.logging import get_logger
from config import settings

logger = get_logger("validate")

MIN_SCORE = settings["validation"]["min_score"]
MAX_SCORE = settings["validation"]["max_score"]


class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class IntegrityWarning:
    check: str
    message: str
    severity: Severity = Severity.WARNING
    details: Optional[dict] = field(default=None)
    
    def __str__(self):
        return f"[{self.check}] {self.message}"
    
    def to_dict(self) -> dict:
        return {
            "check": self.check,
            "message": self.message,
            "severity": self.severity.value,
            "details": self.details,
        }
    
    def is_error(self) -> bool:
        return self.severity == Severity.ERROR


@dataclass
class ValidationResult:
    warnings: list[IntegrityWarning] = field(default_factory=list)
    source_count: int = 0
    target_count: int = 0
    
    def has_errors(self) -> bool:
        return any(w.is_error() for w in self.warnings)
    
    def passed(self) -> bool:
        return not self.has_errors()
    
    def to_list(self) -> list[str]:
        return [str(w) for w in self.warnings]


SOURCE_COUNT_QUERY = text("SELECT COUNT(*) FROM check_results")

TARGET_VALIDATION_QUERY = text("""
    SELECT 
        (SELECT COUNT(*) FROM fact_quality_checks) AS fact_count,
        (SELECT COUNT(*) FROM fact_quality_checks f 
         LEFT JOIN dim_datasets d ON f.dataset_id = d.id 
         WHERE d.id IS NULL) AS orphaned_datasets,
        (SELECT COUNT(*) FROM fact_quality_checks f 
         LEFT JOIN dim_rules r ON f.rule_id = r.id 
         WHERE r.id IS NULL) AS orphaned_rules,
        (SELECT COUNT(*) FROM fact_quality_checks f 
         LEFT JOIN dim_date d ON f.date_key = d.date_key 
         WHERE d.date_key IS NULL) AS orphaned_dates,
        (SELECT COUNT(*) FROM fact_quality_checks 
         WHERE score < :min_score OR score > :max_score) AS invalid_scores
""")


def validate(source_engine: Engine, target_engine: Engine) -> list[IntegrityWarning]:
    logger.info("Starting post-load validation")
    
    result = ValidationResult()
    
    with source_engine.connect() as conn:
        result.source_count = conn.execute(SOURCE_COUNT_QUERY).scalar()
    
    with target_engine.connect() as conn:
        row = conn.execute(
            TARGET_VALIDATION_QUERY,
            {"min_score": MIN_SCORE, "max_score": MAX_SCORE}
        ).fetchone()
        
        result.target_count = row[0]
        orphaned_datasets = row[1]
        orphaned_rules = row[2]
        orphaned_dates = row[3]
        invalid_scores = row[4]
    
    if result.source_count != result.target_count:
        result.warnings.append(IntegrityWarning(
            check="ROW_COUNT",
            message=f"Source: {result.source_count}, Target: {result.target_count}. Delta may indicate multiple ETL runs.",
            severity=Severity.WARNING,
            details={"source": result.source_count, "target": result.target_count},
        ))
    else:
        logger.info("Row counts match: %d", result.source_count)
    
    if orphaned_datasets > 0:
        result.warnings.append(IntegrityWarning(
            check="FK_DATASET",
            message=f"{orphaned_datasets} orphaned dataset references",
            severity=Severity.ERROR,
            details={"count": orphaned_datasets},
        ))
    
    if orphaned_rules > 0:
        result.warnings.append(IntegrityWarning(
            check="FK_RULE",
            message=f"{orphaned_rules} orphaned rule references",
            severity=Severity.ERROR,
            details={"count": orphaned_rules},
        ))
    
    if orphaned_dates > 0:
        result.warnings.append(IntegrityWarning(
            check="FK_DATE",
            message=f"{orphaned_dates} orphaned date references",
            severity=Severity.ERROR,
            details={"count": orphaned_dates},
        ))
    
    if invalid_scores > 0:
        result.warnings.append(IntegrityWarning(
            check="INVALID_SCORE",
            message=f"{invalid_scores} scores outside [{MIN_SCORE}, {MAX_SCORE}]",
            severity=Severity.ERROR,
            details={"count": invalid_scores, "min": MIN_SCORE, "max": MAX_SCORE},
        ))
    
    if result.warnings:
        error_count = sum(1 for w in result.warnings if w.is_error())
        warning_count = len(result.warnings) - error_count
        
        for w in result.warnings:
            if w.is_error():
                logger.error(str(w))
            else:
                logger.warning(str(w))
        
        logger.warning("Validation finished with %d error(s) and %d warning(s)", error_count, warning_count)
    else:
        logger.info("Validation passed - no issues found")
    
    return result.warnings


def validation_passed(warnings: list[IntegrityWarning]) -> bool:
    return not any(w.is_error() for w in warnings)
