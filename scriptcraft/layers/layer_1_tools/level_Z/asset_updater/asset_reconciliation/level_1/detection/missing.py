# ============================================================
# detection/missing.py — missing asset / form mismatch detection
# ============================================================

import pandas as pd

from layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import MERGED


# ------------------------------------------------------------
# MAIN DETECTOR
# ------------------------------------------------------------

def detect_missing(
    merged: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits merged dataset into:

    1. missing_from_form:
        Assets that do not have a matching form entry

    2. only_in_form:
        Form entries that do not match any asset record
    """

    merge_col = MERGED.merge_flag

    if merge_col not in merged.columns:
        raise ValueError(
            "merged dataframe must include merge_flag "
            "(ensure build_merged_dataset was used)"
        )

    left_only = merged[merged[merge_col] == "left_only"].copy()
    right_only = merged[merged[merge_col] == "right_only"].copy()

    # ------------------------------------------------------------
    # ASSET SIDE (missing from form)
    # ------------------------------------------------------------
    missing_from_form = left_only[
        [
            MERGED.tag,
            MERGED.asset_emp_id,
            MERGED.asset_location,
            MERGED.asset_description,
        ]
    ].reset_index(drop=True)

    missing_from_form = missing_from_form.rename(columns={
        MERGED.tag: "tag",
        MERGED.asset_emp_id: "asset_emp_id",
        MERGED.asset_location: "asset_location",
        MERGED.asset_description: "asset_description",
    })

    # ------------------------------------------------------------
    # FORM SIDE (not found in asset DB)
    # ------------------------------------------------------------
    only_in_form = right_only[
        [
            MERGED.tag,
            MERGED.form_emp_id,
            MERGED.form_employee_name,
            MERGED.form_location,
        ]
    ].reset_index(drop=True)

    only_in_form = only_in_form.rename(columns={
        MERGED.tag: "tag",
        MERGED.form_emp_id: "form_emp_id",
        MERGED.form_employee_name: "form_employee_name",
        MERGED.form_location: "form_location",
    })

    return missing_from_form, only_in_form