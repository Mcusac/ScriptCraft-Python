"""Normalization helpers for dataset + dictionary tables."""

import pandas as pd

from typing import Any

from layers.layer_1_tools.level_1_impl.level_5.dictionary_cleaner.normalizer import clean_dictionary


def normalize_dataset_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(c).strip() for c in df.columns]
    return df


def normalize_dictionary_df(dict_df: pd.DataFrame) -> pd.DataFrame:
    dict_df.columns = [str(c).strip() for c in dict_df.columns]
    return clean_dictionary(dict_df, cleaning_level="standard")


def ensure_dataframe(obj: Any, *, label: str) -> pd.DataFrame:
    if not isinstance(obj, pd.DataFrame):
        raise TypeError(f"{label} must be a pandas DataFrame, got: {type(obj)}")
    return obj

