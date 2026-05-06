# ============================================================
# normalizer/tags.py — canonical tag and employee-ID cleaning
#
# Pure functions; safe null handling; deterministic output.
# ============================================================

import pandas as pd


# -----------------------------
# PRIVATE HELPERS
# -----------------------------

def _is_empty(val) -> bool:
    """
    Unified emptiness check for:
    - None
    - NaN
    - pd.NA
    - empty strings
    """
    if val is None:
        return True
    if pd.isna(val):
        return True
    if str(val).strip() == "":
        return True
    if str(val).strip().lower() in {"nan", "none", "na"}:
        return True
    return False


def _fix_tag_format(value) -> str:
    """
    Domain-specific correction rules for a single asset-tag string.

    Rules:
      1. Empty → ""
      2. Remove Excel float artifacts
      3. Remove whitespace
      4. Apply known padding rules
    """

    if _is_empty(value):
        return ""

    v = str(value).strip()

    # Excel artifact cleanup
    if v.endswith(".0"):
        v = v[:-2]

    v = v.replace(" ", "")

    # Defensive: ensure still valid string
    if v == "":
        return ""

    # Domain padding rules
    if len(v) == 5:
        if v.startswith("4"):
            v = "000" + v
        elif v.startswith("3"):
            v = "000" + v

    return v


# -----------------------------
# PUBLIC API
# -----------------------------

def normalize_tag(series: pd.Series) -> pd.Series:
    """
    Vectorised tag normalization.

    NOTE:
    - does NOT coerce to string globally
    - preserves null safety inside helper
    """
    return series.apply(_fix_tag_format)


def normalize_employee_id(series: pd.Series) -> pd.Series:
    """
    Clean employee IDs:
      - remove whitespace
      - remove Excel '.0' artifacts
      - preserve identifier semantics
    """

    def _clean(val):
        if _is_empty(val):
            return ""

        s = str(val).strip()
        s = s.replace(" ", "")
        s = s.rstrip(".0")

        return s

    return series.apply(_clean)