"""Dictionary DataFrame normalizer (schema-level logic only)."""

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_3.dataframe_cleaning import clean_dataframe

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.dictionary_cleaner.value_types import DEFAULT_VALUE_TYPE, VALUE_TYPE_MAP
from scriptcraft.layers.layer_1_tools.level_1_impl.level_3.dictionary_cleaner.expected_values import clean_expected_values

_TEXT_COLUMNS = ("Main Variable", "Value Type", "Expected Values")


# =========================================================
# 🔧 INTERNAL NORMALIZATION HELPERS (SCHEMA ONLY)
# =========================================================

def _standardize_value_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize Value Type using canonical mapping.
    """
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
    """
    Apply domain-specific expected value normalization.
    """
    if "Expected Values" not in df.columns:
        return df

    df["Expected Values"] = df.apply(clean_expected_values, axis=1)
    return df


def _normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Light schema-level text normalization ONLY (no structural cleaning).
    """
    for col in _TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df


# =========================================================
# 🧠 MAIN PIPELINE
# =========================================================

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

    # 1. ALWAYS delegate structural cleanup to infra
    df = clean_dataframe(df)

    # 2. schema-level text cleanup only
    df = _normalize_text_columns(df)

    # 3. value semantics
    df = _standardize_value_types(df)

    # 4. domain-specific parsing
    df = _normalize_expected_values(df)

    return df