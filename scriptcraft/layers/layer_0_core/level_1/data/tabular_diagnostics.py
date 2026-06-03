"""Pure pandas DataFrame diagnostic helpers (no logging)."""

import pandas as pd

from typing import Dict, List, Optional, Set


def get_column_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Generate column statistics (dtype, missing, unique counts)."""
    stats = []
    for col in df.columns:
        unique_count = df[col].nunique()
        missing_count = df[col].isna().sum()
        stats.append({
            "column": col,
            "dtype": str(df[col].dtype),
            "unique_values": unique_count,
            "missing_values": missing_count,
            "missing_percentage": (missing_count / len(df)) * 100,
        })
    return pd.DataFrame(stats)


def get_column_letter(column_number: int) -> str:
    """Convert a 1-based column number to Excel column letters."""
    result = ""
    while column_number > 0:
        column_number -= 1
        result = chr(65 + (column_number % 26)) + result
        column_number //= 26
    return result


def get_common_columns(df1: pd.DataFrame, df2: pd.DataFrame) -> Set[str]:
    return set(df1.columns) & set(df2.columns)


def get_column_dtypes(df: pd.DataFrame) -> Dict[str, str]:
    return {col: str(dtype) for col, dtype in df.dtypes.items()}


def compare_column_dtypes(df1: pd.DataFrame, df2: pd.DataFrame) -> Dict[str, tuple]:
    common_cols = get_common_columns(df1, df2)
    return {
        col: (str(df1[col].dtype), str(df2[col].dtype))
        for col in common_cols
    }


def find_duplicate_rows(
    df: pd.DataFrame,
    subset: Optional[List[str]] = None,
) -> pd.DataFrame:
    return df[df.duplicated(subset=subset, keep=False)].sort_values(
        by=subset or df.columns.tolist()
    )


def drop_empty_columns(df: pd.DataFrame, threshold: float = 1.0) -> pd.DataFrame:
    null_frac = df.isnull().mean()
    cols_to_drop = null_frac[null_frac >= threshold].index
    return df.drop(columns=cols_to_drop)


def to_numeric_safe(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def find_non_numeric(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    return series[numeric.isna() & series.notna()].unique()


def describe_numeric(df: pd.DataFrame, include_nulls: bool = True) -> pd.DataFrame:
    stats = df.describe()
    if include_nulls:
        stats.loc["null_count"] = df.isnull().sum()
        stats.loc["null_pct"] = df.isnull().mean()
    return stats