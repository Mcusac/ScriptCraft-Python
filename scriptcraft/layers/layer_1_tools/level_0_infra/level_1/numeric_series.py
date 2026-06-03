"""Numeric series extraction for dictionary/QC tools (uses core cleaning + tools logging)."""

import pandas as pd

from scriptcraft.layers.layer_0_core.level_2 import clean_numeric_column_series

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print


def get_clean_numeric_series(df: pd.DataFrame, col: str) -> pd.Series:
    """Extract numeric-only cleaned series from a column."""
    if col not in df.columns:
        return pd.Series(dtype=float)

    before_len = len(df[col])
    numeric = clean_numeric_column_series(df, col)
    dropped = before_len - len(numeric)
    if dropped > 0:
        log_and_print(
            f"⚠️ Removed {dropped} non-numeric values from '{col}'"
        )

    return numeric
