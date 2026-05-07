# ============================================================
# string_normalizer.py — canonical comparison normalization
# ============================================================

import pandas as pd


# ============================================================
# NULL NORMALIZATION
# ============================================================

_NULL_STRINGS = {"", "nan", "none", "na"}


def normalize_string(value) -> str:
    """
    Canonical comparison-safe string normalization.

    Rules:
    - null → ""
    - trim whitespace
    - lowercase
    - normalize textual nulls
    """

    if value is None or pd.isna(value):
        return ""

    normalized = str(value).strip().lower()

    if normalized in _NULL_STRINGS:
        return ""

    return normalized