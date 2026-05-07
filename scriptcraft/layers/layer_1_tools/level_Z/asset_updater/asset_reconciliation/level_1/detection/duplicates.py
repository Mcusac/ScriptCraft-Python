# ============================================================
# detection/duplicates.py — duplicate form-tag detection
#
# DESIGN:
# - Pure detector layer
# - Schema-driven
# - DAG-safe validation
# - Reusable projection pipeline
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import (
    FORM_RAW_TAG,
    FORM_RAW_EMP_ID,
    FORM_RAW_FIRST_NAME,
    FORM_RAW_LAST_NAME,
    FORM_RAW_LOCATION,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.validators import (
    require_columns,
)


# ============================================================
# OUTPUT CONTRACT
# ============================================================

DUPLICATE_OUTPUT_COLUMNS = [
    FORM_RAW_TAG,
    FORM_RAW_EMP_ID,
    FORM_RAW_FIRST_NAME,
    FORM_RAW_LAST_NAME,
    FORM_RAW_LOCATION,
]


# ============================================================
# INTERNAL HELPERS
# ============================================================

def _get_duplicate_rows(
    df: pd.DataFrame,
    key_column: str,
) -> pd.DataFrame:
    """
    Returns all duplicated rows for a key column.
    """

    duplicate_mask = df.duplicated(
        subset=[key_column],
        keep=False,
    )

    return df[duplicate_mask].copy()


def _project_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Safe output projection layer.
    """

    available = [c for c in columns if c in df.columns]

    return df[available].copy()


# ============================================================
# PUBLIC API
# ============================================================

def detect_form_duplicates(
    form_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Detect duplicated device tags in normalized form data.

    Assumes:
    - ingestion mapping already applied
    - dataframe already reshaped
    """

    # --------------------------------------------------------
    # CONTRACT VALIDATION
    # --------------------------------------------------------

    require_columns(
        form_df,
        [FORM_RAW_TAG],
        context="FORM_DUPLICATE_DETECTION",
    )

    # --------------------------------------------------------
    # DETECT DUPLICATES
    # --------------------------------------------------------

    duplicates = _get_duplicate_rows(
        form_df,
        FORM_RAW_TAG,
    )

    # --------------------------------------------------------
    # EMPTY CONTRACT
    # --------------------------------------------------------

    if duplicates.empty:
        return pd.DataFrame(columns=DUPLICATE_OUTPUT_COLUMNS)

    # --------------------------------------------------------
    # OUTPUT PROJECTION
    # --------------------------------------------------------

    duplicates = _project_columns(
        duplicates,
        DUPLICATE_OUTPUT_COLUMNS,
    )

    return (
        duplicates
        .sort_values(FORM_RAW_TAG)
        .reset_index(drop=True)
    )