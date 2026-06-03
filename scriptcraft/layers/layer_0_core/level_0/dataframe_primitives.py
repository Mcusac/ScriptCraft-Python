"""Reusable DataFrame projection and predicate primitives."""

import pandas as pd

from typing import Any, Dict, List, Optional


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


def outer_merge_with_indicator(
    left: pd.DataFrame,
    right: pd.DataFrame,
    *,
    left_on: str,
    right_on: str,
    indicator_col: str = "merge_flag",
) -> pd.DataFrame:
    """Outer merge with pandas indicator, renaming ``_merge`` to ``indicator_col``."""
    merged = pd.merge(
        left,
        right,
        left_on=left_on,
        right_on=right_on,
        how="outer",
        indicator=True,
        validate="many_to_many",
    )
    return merged.rename(columns={"_merge": indicator_col})


def get_dataframe_summary(df: pd.DataFrame, key_col: str | None = None) -> dict:
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "unique_keys": df[key_col].nunique() if key_col and key_col in df.columns else None,
        "null_counts": df.isna().sum().to_dict(),
    }


def get_merge_summary(df: pd.DataFrame, merge_col: str = "_merge") -> dict:
    if merge_col not in df.columns:
        return {"error": "missing_merge_column"}

    return {
        "distribution": df[merge_col].value_counts().to_dict(),
        "sample": df[[merge_col]].head(10).to_dict(orient="records"),
    }


def shallow_compare_dataframes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    compare_columns: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Compare shapes and column sets without row-level diff."""
    comparison: Dict[str, Any] = {
        "shape_difference": df1.shape != df2.shape,
        "df1_shape": df1.shape,
        "df2_shape": df2.shape,
        "column_differences": set(df1.columns) ^ set(df2.columns),
        "common_columns": set(df1.columns) & set(df2.columns),
    }

    if compare_columns:
        comparison["column_differences"] = (
            set(compare_columns) ^ set(df1.columns) ^ set(df2.columns)
        )

    return comparison
