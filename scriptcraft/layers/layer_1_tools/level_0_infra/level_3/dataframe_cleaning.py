"""
DataFrame structural cleaning + generic column utilities
"""

import pandas as pd

from typing import Dict

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_2.value_cleaning import is_missing_like


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Canonical DataFrame cleanup (ONLY structural concerns).

    Responsibilities:
    - remove unnamed columns
    - drop empty columns
    - normalize NaN → ""
    """
    if df is None:
        raise ValueError("df must not be None")

    return (
        df.copy()
        .loc[:, ~df.columns.astype(str).str.contains("^Unnamed", na=False)]
        .dropna(axis=1, how="all")
        .fillna("")
    )


def standardize_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Rename columns using mapping (no validation logic beyond rename).
    """
    renamed = df.rename(columns=mapping)

    missing_expected = [v for v in mapping.values() if v not in renamed.columns]
    if missing_expected:
        log_and_print(f"⚠️ Missing expected columns: {missing_expected}")

    return renamed


def parse_missing_unit(value):
    """
    Normalize unit formatting (light regex cleanup only).
    """
    import re

    if pd.isna(value) or isinstance(value, (int, float)):
        return value

    return re.sub(r"=\s*", "= ", str(value))


def get_clean_numeric_series(df: pd.DataFrame, col: str) -> pd.Series:
    """
    Extract numeric-only cleaned series from column.
    """
    if col not in df.columns:
        return pd.Series(dtype=float)

    series = df[col]

    series = series[~series.apply(is_missing_like)]
    numeric = pd.to_numeric(series, errors="coerce").dropna()

    if len(series) != len(numeric):
        log_and_print(
            f"⚠️ Removed {len(series) - len(numeric)} non-numeric values from '{col}'"
        )

    return numeric