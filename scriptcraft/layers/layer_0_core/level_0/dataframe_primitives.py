"""Reusable DataFrame projection and predicate primitives."""

import pandas as pd


def project_columns_required(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Schema-strict projection that requires all requested columns."""
    return df[columns].reset_index(drop=True)


def project_columns_available(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Safe projection that keeps only columns that exist."""
    available = [column for column in columns if column in df.columns]
    return df[available].copy()


def safe_eq(
    df: pd.DataFrame,
    col: str,
    value: str,
) -> pd.Series:
    """Null-safe equality comparison; missing columns return all-False."""
    if col not in df.columns:
        return pd.Series(False, index=df.index)

    return df[col].astype("string").eq(value)
