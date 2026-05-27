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

from scriptcraft.layers.layer_0_core.level_0 import project_columns_available, require_columns

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import FORM_RAW

# ============================================================
# OUTPUT CONTRACT
# ============================================================

DUPLICATE_OUTPUT_COLUMNS = [
    FORM_RAW.tag,
    FORM_RAW.emp_id,
    FORM_RAW.first_name,
    FORM_RAW.last_name,
    FORM_RAW.location,
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
        [FORM_RAW.tag],
        context="FORM_DUPLICATE_DETECTION",
    )

    # --------------------------------------------------------
    # DETECT DUPLICATES
    # --------------------------------------------------------

    duplicates = _get_duplicate_rows(
        form_df,
        FORM_RAW.tag,
    )

    # --------------------------------------------------------
    # EMPTY CONTRACT
    # --------------------------------------------------------

    if duplicates.empty:
        return pd.DataFrame(columns=DUPLICATE_OUTPUT_COLUMNS)

    # --------------------------------------------------------
    # OUTPUT PROJECTION
    # --------------------------------------------------------

    duplicates = project_columns_available(
        duplicates,
        DUPLICATE_OUTPUT_COLUMNS,
    )

    return (
        duplicates
        .sort_values(FORM_RAW.tag)
        .reset_index(drop=True)
    )