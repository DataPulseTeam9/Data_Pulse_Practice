from typing import Optional
import numpy as np
import pandas as pd

from pipeline.utils.logging import get_logger
from config import settings

logger = get_logger("transform")


class ValidationError(Exception):
    pass


class TransformResult:
    def __init__(
        self,
        dim_datasets: pd.DataFrame,
        dim_rules: pd.DataFrame,
        dim_date: pd.DataFrame,
        facts: pd.DataFrame
    ):
        self.dim_datasets = dim_datasets
        self.dim_rules = dim_rules
        self.dim_date = dim_date
        self.facts = facts
    
    def to_dict(self) -> dict:
        return {
            "dim_datasets": self.dim_datasets,
            "dim_rules": self.dim_rules,
            "dim_date": self.dim_date,
            "facts": self.facts,
        }
    
    def __repr__(self):
        return (
            f"TransformResult(datasets={len(self.dim_datasets)}, "
            f"rules={len(self.dim_rules)}, dates={len(self.dim_date)}, "
            f"facts={len(self.facts)})"
        )


DIM_DATASET_MAPPING = settings["schema"]["dim_dataset_mapping"]
DIM_RULE_MAPPING = settings["schema"]["dim_rule_mapping"]
REQUIRED_COLUMNS = settings["validation"]["required_columns"]


def validate_raw_data(df: pd.DataFrame) -> list[str]:
    warnings = []
    
    if df is None or df.empty:
        raise ValidationError("Input DataFrame is empty")
    
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValidationError(f"Missing required columns: {missing}")
    
    for col in REQUIRED_COLUMNS:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            warnings.append(f"Column '{col}' has {null_count} null values")
            logger.warning("Column '%s' has %d null values", col, null_count)
    
    invalid_count = (df["total_rows"] <= 0).sum()
    if invalid_count > 0:
        warnings.append(f"{invalid_count} records have total_rows <= 0")
        logger.warning("%d records have total_rows <= 0", invalid_count)
    
    return warnings


def transform(raw_data: pd.DataFrame) -> Optional[dict]:
    if raw_data is None or raw_data.empty:
        logger.warning("No data to transform")
        return None
    
    validate_raw_data(raw_data)
    
    logger.info("Transforming %d raw records", len(raw_data))

    result = TransformResult(
        dim_datasets=_build_dim_datasets(raw_data),
        dim_rules=_build_dim_rules(raw_data),
        dim_date=_build_dim_date(raw_data),
        facts=_build_facts(raw_data),
    )

    logger.info("Transform complete - %s", result)
    return result.to_dict()


def _build_dim_datasets(df: pd.DataFrame) -> pd.DataFrame:
    cols = list(DIM_DATASET_MAPPING.keys())
    dim = df[cols].drop_duplicates(subset=["dataset_id"]).copy()
    dim.rename(columns=DIM_DATASET_MAPPING, inplace=True)
    return dim.reset_index(drop=True)


def _build_dim_rules(df: pd.DataFrame) -> pd.DataFrame:
    cols = list(DIM_RULE_MAPPING.keys())
    dim = df[cols].drop_duplicates(subset=["rule_id"]).copy()
    dim.rename(columns=DIM_RULE_MAPPING, inplace=True)
    return dim.reset_index(drop=True)


def _build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    try:
        dates = pd.to_datetime(df["checked_at"], errors="coerce")
        
        valid_dates = dates.dropna()
        if valid_dates.empty:
            logger.warning("No valid dates found in checked_at column")
            return pd.DataFrame(columns=["date_key", "full_date", "day_of_week", "month", "quarter", "year"])
        
        min_date = valid_dates.min()
        max_date = valid_dates.max()
        
        date_range = pd.date_range(start=min_date.normalize(), end=max_date.normalize(), freq="D")
        
        dim = pd.DataFrame({
            "date_key": (date_range.year * 10000 + date_range.month * 100 + date_range.day).astype(int),
            "full_date": date_range.date,
            "day_of_week": date_range.dayofweek.astype(int),
            "month": date_range.month.astype(int),
            "quarter": date_range.quarter.astype(int),
            "year": date_range.year.astype(int),
        })
        return dim
        
    except Exception as e:
        logger.error("Failed to build date dimension: %s", e)
        raise ValidationError(f"Date dimension build failed: {e}") from e


def _build_facts(df: pd.DataFrame) -> pd.DataFrame:
    facts = df[["id", "dataset_id", "rule_id", "passed", "failed_rows", "total_rows", "checked_at"]].copy()
    
    total_rows = facts["total_rows"].values
    failed_rows = facts["failed_rows"].values
    
    with np.errstate(divide="ignore", invalid="ignore"):
        score = np.where(
            total_rows > 0,
            np.round((total_rows - failed_rows) / total_rows * 100, 2),
            0.0
        )
    facts["score"] = score
    
    checked_at = pd.to_datetime(facts["checked_at"], errors="coerce")
    facts["date_key"] = (
        checked_at.dt.year * 10000 +
        checked_at.dt.month * 100 +
        checked_at.dt.day
    ).fillna(0).astype(int)
    
    return facts.reset_index(drop=True)
