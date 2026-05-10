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

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import (
    MERGED,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.validators import (
    require_columns,
)


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


def _project_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Stable schema-safe projection.
    """

    return (
        df[columns]
        .reset_index(drop=True)
    )


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

    missing_from_form = _project_columns(
        left_only,
        _MISSING_FROM_FORM_COLUMNS,
    )

    only_in_form = _project_columns(
        right_only,
        _ONLY_IN_FORM_COLUMNS,
    )

    return (
        missing_from_form,
        only_in_form,
    )