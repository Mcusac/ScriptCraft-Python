# ============================================================
# predicates.py — reusable dataframe predicates
# ============================================================

import pandas as pd


def safe_eq(
    df: pd.DataFrame,
    col: str,
    value: str,
) -> pd.Series:
    """
    Null-safe equality comparison.

    Missing columns return an all-False mask.
    """

    if col not in df.columns:
        return pd.Series(False, index=df.index)

    return df[col].astype("string").eq(value)