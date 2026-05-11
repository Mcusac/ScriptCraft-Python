# ============================================================
# validators.py — dataframe contract enforcement layer
#
# DESIGN:
# - Single responsibility:
#     schema contract enforcement only
# - Pure validation utilities
# - DAG-stage boundary guards
# - No dataframe mutation
# - No business logic
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_0.schema import (
    ASSET_RAW,
    FORM_NORMALIZED,
    FORM_RAW,
    MERGED,
)


# ============================================================
# SCHEMA CONTRACT REGISTRY
# ============================================================

_ASSET_RAW_COLUMNS = [
    ASSET_RAW.tag,
    ASSET_RAW.emp_id,
    ASSET_RAW.location,
    ASSET_RAW.custodian,
    ASSET_RAW.description,
]

_FORM_RAW_COLUMNS = [
    FORM_RAW.tag,
    FORM_RAW.emp_id,
    FORM_RAW.first_name,
    FORM_RAW.last_name,
    FORM_RAW.location,
]

_FORM_NORMALIZED_COLUMNS = [
    FORM_NORMALIZED.tag,
    FORM_NORMALIZED.emp_id,
    FORM_NORMALIZED.location,
    FORM_NORMALIZED.employee_name,
]

_MERGED_COLUMNS = [
    MERGED.tag,
    MERGED.asset_emp_id,
    MERGED.asset_location,
    MERGED.asset_custodian,
    MERGED.asset_description,
    MERGED.form_emp_id,
    MERGED.form_employee_name,
    MERGED.form_location,
    MERGED.merge_flag,
]


# ============================================================
# CORE VALIDATION ENGINE
# ============================================================

def require_columns(
    df: pd.DataFrame,
    required: list[str],
    context: str = "",
) -> None:
    """
    Ensures required columns exist.
    """

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise RuntimeError(
            f"[SCHEMA ERROR] Missing columns in "
            f"{context}: {missing}"
        )


def require_exact_columns(
    df: pd.DataFrame,
    required: list[str],
    context: str = "",
) -> None:
    """
    Enforces exact schema contract.
    Prevents silent schema drift.
    """

    actual = set(df.columns)
    expected = set(required)

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)

    if missing or extra:
        raise RuntimeError(
            f"[SCHEMA VIOLATION] {context}\n"
            f"Missing: {missing}\n"
            f"Unexpected: {extra}"
        )


# ============================================================
# DAG STAGE VALIDATORS
# ============================================================

def assert_asset_raw(
    df: pd.DataFrame,
) -> None:
    """
    Validates ASSET_RAW contract.
    """

    require_columns(
        df,
        _ASSET_RAW_COLUMNS,
        context="ASSET_RAW",
    )


def assert_form_raw(
    df: pd.DataFrame,
) -> None:
    """
    Validates FORM_RAW contract.
    """

    require_columns(
        df,
        _FORM_RAW_COLUMNS,
        context="FORM_RAW",
    )


def assert_form_normalized(
    df: pd.DataFrame,
) -> None:
    """
    Validates FORM_NORMALIZED contract.
    """

    require_columns(
        df,
        _FORM_NORMALIZED_COLUMNS,
        context="FORM_NORMALIZED",
    )


def assert_merged(
    df: pd.DataFrame,
) -> None:
    """
    Validates final MERGED contract.
    """

    require_exact_columns(
        df,
        _MERGED_COLUMNS,
        context="MERGED",
    )