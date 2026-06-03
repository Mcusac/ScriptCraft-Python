"""Pure pandas comparison operations (no logging or filesystem side effects)."""

import pandas as pd

from typing import Any, Dict, Iterable, Optional, Set, Tuple, Union


def column_sets(
    df1: Union[pd.DataFrame, Set[Any]],
    df2: Union[pd.DataFrame, Set[Any]],
) -> Tuple[Set[str], Set[str], Set[str]]:
    cols_a = (
        set(df1.columns)
        if isinstance(df1, pd.DataFrame)
        else set(df1)
    )
    cols_b = (
        set(df2.columns)
        if isinstance(df2, pd.DataFrame)
        else set(df2)
    )
    common = cols_a & cols_b
    only_a = cols_a - cols_b
    only_b = cols_b - cols_a
    return common, only_a, only_b


def dtype_mismatches(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
) -> Dict[str, Tuple[Any, Any]]:
    common_cols = set(df1.columns) & set(df2.columns)
    return {
        col: (df1[col].dtype, df2[col].dtype)
        for col in common_cols
        if df1[col].dtype != df2[col].dtype
    }


def content_differences(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
) -> Optional[pd.DataFrame]:
    common_cols = df1.columns.intersection(df2.columns)
    differences = df1[common_cols].compare(df2[common_cols])
    if differences.empty:
        return None
    return differences


def shape_mismatch(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    if df1.shape == df2.shape:
        return None
    return (df1.shape, df2.shape)


def index_sets(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
) -> Tuple[Set[Any], Set[Any], Set[Any]]:
    idx_1 = set(df1.index)
    idx_2 = set(df2.index)
    common = idx_1 & idx_2
    only_1 = idx_1 - idx_2
    only_2 = idx_2 - idx_1
    return common, only_1, only_2


def compute_case_mismatches(
    left: Iterable[str],
    right: Iterable[str],
) -> Tuple[Tuple[str, str], ...]:
    """Return pairs that match case-insensitively but differ in casing."""
    left_by_lower = {value.lower(): value for value in left}
    right_by_lower = {value.lower(): value for value in right}
    mismatches: list[Tuple[str, str]] = []

    for key in left_by_lower.keys() & right_by_lower.keys():
        left_value = left_by_lower[key]
        right_value = right_by_lower[key]
        if left_value != right_value:
            mismatches.append((left_value, right_value))

    return tuple(mismatches)
