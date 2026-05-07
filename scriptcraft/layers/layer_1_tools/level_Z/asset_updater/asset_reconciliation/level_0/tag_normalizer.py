# ============================================================
# tag_normalizer.py — canonical identifier normalization
# ============================================================

import pandas as pd


# ============================================================
# 1. NULL NORMALIZATION
# ============================================================

_NULL_STRINGS = {"nan", "none", "na", ""}


def is_empty(val) -> bool:
    if val is None:
        return True
    if pd.isna(val):
        return True

    if isinstance(val, str):
        return val.strip().lower() in _NULL_STRINGS

    return False


# ============================================================
# 2. SANITIZATION LAYER (PURE TRANSFORM)
# ============================================================

def sanitize(value) -> str:
    """
    Converts raw input → clean string base.
    No domain logic allowed here.
    """

    if is_empty(value):
        return ""

    s = str(value).strip()

    if s.endswith(".0"):
        s = s[:-2]

    return s.replace(" ", "")


# ============================================================
# 3. DOMAIN RULES (TAG ONLY)
# ============================================================

def apply_tag_rules(value: str) -> str:
    """
    Domain-specific rules for asset tags only.
    Requires sanitized input.
    """

    if not value:
        return ""

    # padding rule (business logic)
    if len(value) == 5 and value[0] in {"3", "4"}:
        return "000" + value

    return value


# ============================================================
# 4. PIPELINE COMPOSER (IMPORTANT DAG FIX)
# ============================================================

def _tag_pipeline(value) -> str:
    """
    Explicit DAG-style transformation pipeline.
    """

    return apply_tag_rules(sanitize(value))


def _id_pipeline(value) -> str:
    """
    Employee ID pipeline (no domain logic).
    """

    return sanitize(value)


# ============================================================
# 5. PUBLIC API
# ============================================================

def normalize_tag(series: pd.Series) -> pd.Series:
    return series.map(_tag_pipeline)


def normalize_employee_id(series: pd.Series) -> pd.Series:
    return series.map(_id_pipeline)