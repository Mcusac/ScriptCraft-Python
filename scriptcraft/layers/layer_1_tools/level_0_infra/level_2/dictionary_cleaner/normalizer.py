"""Dictionary DataFrame normalizer (schema-level logic only)."""

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    DEFAULT_VALUE_TYPE,
    VALUE_TYPE_MAP,
    clean_expected_values,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import clean_dataframe

_TEXT_COLUMNS = ("Main Variable", "Value Type", "Expected Values")


def _standardize_value_types(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize Value Type using canonical mapping."""
    if "Value Type" not in df.columns:
        return df

    df["Value Type"] = (
        df["Value Type"]
        .astype(str)
        .str.lower()
        .map(VALUE_TYPE_MAP)
        .fillna(DEFAULT_VALUE_TYPE)
    )
    return df


def _normalize_expected_values(df: pd.DataFrame) -> pd.DataFrame:
    """Apply domain-specific expected value normalization."""
    if "Expected Values" not in df.columns:
        return df

    df["Expected Values"] = df.apply(clean_expected_values, axis=1)
    return df


def _normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Light schema-level text normalization ONLY (no structural cleaning)."""
    for col in _TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df


def clean_dictionary(df: pd.DataFrame, *, cleaning_level: str = "standard") -> pd.DataFrame:
    """
    Normalize dictionary DataFrame (schema-level transformation only).

    Pipeline order:
    1. structural cleanup (infra)
    2. text normalization (light)
    3. value type standardization
    4. expected value parsing
    """
    _ = cleaning_level

    if df is None:
        raise ValueError("df must not be None")

    df = clean_dataframe(df)
    df = _normalize_text_columns(df)
    df = _standardize_value_types(df)
    df = _normalize_expected_values(df)

    return df
