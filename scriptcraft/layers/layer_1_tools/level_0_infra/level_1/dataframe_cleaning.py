"""
DataFrame structural cleaning + generic column utilities
"""

import re
import pandas as pd

from typing import Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Canonical DataFrame cleanup (ONLY structural concerns).

    Responsibilities:
    - remove unnamed columns
    - drop empty columns
    - normalize NaN → ""
    """
    if df is None:
        raise ValueError("df must not be None")

    return (
        df.copy()
        .loc[:, ~df.columns.astype(str).str.contains("^Unnamed", na=False)]
        .dropna(axis=1, how="all")
        .fillna("")
    )


def standardize_columns(
    df: pd.DataFrame,
    mapping: Dict[str, str],
    *,
    strict: bool = False,
) -> pd.DataFrame:
    """
    Rename columns using mapping.

    strict=False (default): warn when mapped target names are absent after rename.
    strict=True: raise when any mapping source key is missing from the input frame.
    """
    if strict:
        missing_sources = [
            source
            for source in mapping
            if source not in df.columns
        ]
        if missing_sources:
            raise RuntimeError(
                f"[SCHEMA ERROR] Missing raw columns: {missing_sources}"
            )

    renamed = df.rename(columns=mapping)

    if strict:
        return renamed

    missing_expected = [
        target
        for target in mapping.values()
        if target not in renamed.columns
    ]
    if missing_expected:
        log_and_print(f"⚠️ Missing expected columns: {missing_expected}")

    return renamed


def parse_missing_unit(value):
    """
    Normalize unit formatting (light regex cleanup only).
    """
    if pd.isna(value) or isinstance(value, (int, float)):
        return value

    return re.sub(r"=\s*", "= ", str(value))