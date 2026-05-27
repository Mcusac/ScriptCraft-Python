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

from scriptcraft.layers.layer_0_core.level_0 import (
    require_columns,
    require_exact_columns,
)

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
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


def _validate_contract(
    df: pd.DataFrame,
    required: list[str],
    context: str,
    *,
    exact: bool,
) -> None:
    if exact:
        require_exact_columns(df, required, context=context)
        return

    require_columns(df, required, context=context)


# ============================================================
# DAG STAGE VALIDATORS
# ============================================================

def assert_asset_raw(
    df: pd.DataFrame,
) -> None:
    """
    Validates ASSET_RAW contract.
    """

    _validate_contract(
        df,
        _ASSET_RAW_COLUMNS,
        context="ASSET_RAW",
        exact=False,
    )


def assert_form_raw(
    df: pd.DataFrame,
) -> None:
    """
    Validates FORM_RAW contract.
    """

    _validate_contract(
        df,
        _FORM_RAW_COLUMNS,
        context="FORM_RAW",
        exact=False,
    )


def assert_form_normalized(
    df: pd.DataFrame,
) -> None:
    """
    Validates FORM_NORMALIZED contract.
    """

    _validate_contract(
        df,
        _FORM_NORMALIZED_COLUMNS,
        context="FORM_NORMALIZED",
        exact=False,
    )


def assert_merged(
    df: pd.DataFrame,
) -> None:
    """
    Validates final MERGED contract.
    """

    _validate_contract(
        df,
        _MERGED_COLUMNS,
        context="MERGED",
        exact=True,
    )
