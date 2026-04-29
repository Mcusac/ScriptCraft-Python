"""Pure DataFrame normalizer for dictionary tables."""

import pandas as pd

from .expected_values import clean_expected_values
from .value_types import DEFAULT_VALUE_TYPE, VALUE_TYPE_MAP

_TEXT_COLUMNS = ("Main Variable", "Value Type", "Expected Values")


def _strip_text_columns(df: pd.DataFrame) -> None:
    for col in _TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()


def _standardize_value_types(df: pd.DataFrame) -> None:
    if "Value Type" not in df.columns:
        return
    df["Value Type"] = (
        df["Value Type"].str.lower().map(VALUE_TYPE_MAP).fillna(DEFAULT_VALUE_TYPE)
    )


def _normalize_expected_values(df: pd.DataFrame) -> None:
    if "Expected Values" in df.columns:
        df["Expected Values"] = df.apply(clean_expected_values, axis=1)


def clean_dictionary(df: pd.DataFrame, *, cleaning_level: str = "standard") -> pd.DataFrame:
    """
    Normalize a dictionary DataFrame in place and return it.

    The `cleaning_level` parameter is currently a stable extension point;
    the standard pipeline runs regardless of level so callers can introduce
    new levels without breaking the API.
    """
    _ = cleaning_level
    df.columns = [col.strip() for col in df.columns]
    _strip_text_columns(df)
    _standardize_value_types(df)
    _normalize_expected_values(df)
    return df
