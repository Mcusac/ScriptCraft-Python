"""Prepare a numeric series for outlier detection."""

import pandas as pd

from scriptcraft.layers.layer_0_core.level_1 import is_missing_like


def clean_numeric_column_series(df: pd.DataFrame, col: str) -> pd.Series:
    """Drop missing-like values and coerce to numeric; NaNs removed."""
    if col not in df.columns:
        return pd.Series(dtype=float)
    series = df[col]
    series = series[~series.map(is_missing_like)]
    return pd.to_numeric(series, errors="coerce").dropna()
