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

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.constants import (
    ASSET_RAW_CUSTODIAN,
    ASSET_RAW_DESCRIPTION,
    ASSET_RAW_EMP_ID,
    ASSET_RAW_LOCATION,
    ASSET_RAW_TAG,
    FORM_NORMALIZED_EMPLOYEE_NAME,
    FORM_RAW_EMP_ID,
    FORM_RAW_FIRST_NAME,
    FORM_RAW_LAST_NAME,
    FORM_RAW_LOCATION,
    FORM_RAW_TAG,
    MERGED_ASSET_CUSTODIAN,
    MERGED_ASSET_DESCRIPTION,
    MERGED_ASSET_EMP_ID,
    MERGED_ASSET_LOCATION,
    MERGED_FLAG,
    MERGED_FORM_EMPLOYEE_NAME,
    MERGED_FORM_EMP_ID,
    MERGED_FORM_LOCATION,
    MERGED_TAG,
)


# ============================================================
# SCHEMA CONTRACT REGISTRY
# ============================================================

_ASSET_RAW_COLUMNS = [
    ASSET_RAW_TAG,
    ASSET_RAW_EMP_ID,
    ASSET_RAW_LOCATION,
    ASSET_RAW_CUSTODIAN,
    ASSET_RAW_DESCRIPTION,
]

_FORM_RAW_COLUMNS = [
    FORM_RAW_TAG,
    FORM_RAW_EMP_ID,
    FORM_RAW_FIRST_NAME,
    FORM_RAW_LAST_NAME,
    FORM_RAW_LOCATION,
]

_FORM_NORMALIZED_COLUMNS = [
    FORM_RAW_TAG,
    FORM_RAW_EMP_ID,
    FORM_RAW_LOCATION,
    FORM_NORMALIZED_EMPLOYEE_NAME,
]

_MERGED_COLUMNS = [
    MERGED_TAG,
    MERGED_ASSET_EMP_ID,
    MERGED_ASSET_LOCATION,
    MERGED_ASSET_CUSTODIAN,
    MERGED_ASSET_DESCRIPTION,
    MERGED_FORM_EMP_ID,
    MERGED_FORM_EMPLOYEE_NAME,
    MERGED_FORM_LOCATION,
    MERGED_FLAG,
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