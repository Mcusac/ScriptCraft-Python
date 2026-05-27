# ============================================================
# detection/missing.py — merged mismatch detectors
#
# DESIGN:
# - Pure detector layer
# - Schema-driven projections
# - DAG-safe validation
# - Stable output contracts
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_0_core.level_0 import (
    project_columns_required,
    require_columns,
)

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import MERGED


# ============================================================
# MERGE STATES
# ============================================================

_LEFT_ONLY = "left_only"
_RIGHT_ONLY = "right_only"


# ============================================================
# OUTPUT CONTRACTS
# ============================================================

_MISSING_FROM_FORM_COLUMNS = [
    MERGED.tag,
    MERGED.asset_emp_id,
    MERGED.asset_location,
    MERGED.asset_description,
]

_ONLY_IN_FORM_COLUMNS = [
    MERGED.tag,
    MERGED.form_emp_id,
    MERGED.form_employee_name,
    MERGED.form_location,
]


# ============================================================
# INTERNAL HELPERS
# ============================================================

def _filter_merge_state(
    merged: pd.DataFrame,
    merge_state: str,
) -> pd.DataFrame:
    """
    Returns rows matching a merge state.
    """

    return merged[
        merged[MERGED.merge_flag] == merge_state
    ].copy()


# ============================================================
# PUBLIC API
# ============================================================

def detect_missing(
    merged: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits merged dataset into:

    1. missing_from_form
        Assets missing from form data

    2. only_in_form
        Form entries missing from asset inventory
    """

    require_columns(
        merged,
        [MERGED.merge_flag],
        context="MISSING_DETECTION",
    )

    # --------------------------------------------------------
    # SPLIT MERGE STATES
    # --------------------------------------------------------

    left_only = _filter_merge_state(
        merged,
        _LEFT_ONLY,
    )

    right_only = _filter_merge_state(
        merged,
        _RIGHT_ONLY,
    )

    # --------------------------------------------------------
    # PROJECT OUTPUT CONTRACTS
    # --------------------------------------------------------

    missing_from_form = project_columns_required(
        left_only,
        _MISSING_FROM_FORM_COLUMNS,
    )

    only_in_form = project_columns_required(
        right_only,
        _ONLY_IN_FORM_COLUMNS,
    )

    return (
        missing_from_form,
        only_in_form,
    )