# ============================================================
# detection/duplicates.py — duplicate Device Tag detection
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import FORM_RAW


# ------------------------------------------------------------
# CORE DETECTOR
# ------------------------------------------------------------

def detect_form_duplicates(form_df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect duplicate Device Tags in normalized form data.

    Assumes:
        - form_df is already standardized to canonical schema
        - ingestion mapping has already been applied
    """

    tag_col = FORM_RAW.tag

    # --------------------------------------------------------
    # Guard: schema contract validation
    # --------------------------------------------------------
    if tag_col not in form_df.columns:
        return pd.DataFrame(columns=[tag_col])

    # --------------------------------------------------------
    # Detect duplicates
    # --------------------------------------------------------
    dupes = form_df[
        form_df.duplicated(subset=[tag_col], keep=False)
    ].copy()

    if dupes.empty:
        return pd.DataFrame(columns=dupes.columns)

    # --------------------------------------------------------
    # Output projection (schema-safe fields only)
    # --------------------------------------------------------
    preferred_cols = [
        FORM_RAW.tag,
        FORM_RAW.emp_id,
        FORM_RAW.first_name,
        FORM_RAW.last_name,
        FORM_RAW.location,
    ]

    available_cols = [c for c in preferred_cols if c in dupes.columns]

    return (
        dupes[available_cols]
        .sort_values(tag_col)
        .reset_index(drop=True)
    )