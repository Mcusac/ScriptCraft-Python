# ============================================================
# detection/changes.py — schema-driven comparison detectors
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import MERGED

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.string_normalizer import (
    normalize_string,
)


# ============================================================
# INTERNAL FILTER
# ============================================================

def _get_both_rows(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Restrict comparison space to matched records only.
    """

    return merged[
        merged[MERGED.MERGE_FLAG] == "both"
    ].copy()


# ============================================================
# LOCATION CHANGES
# ============================================================

def detect_location_changes(merged: pd.DataFrame) -> pd.DataFrame:

    both = _get_both_rows(merged)

    asset_col = MERGED.ASSET_LOCATION
    form_col = MERGED.FORM_LOCATION

    missing = {asset_col, form_col} - set(both.columns)

    if missing:
        raise RuntimeError(f"Missing merged columns: {missing}")

    changed_mask = (
        both[asset_col].map(normalize_string)
        != both[form_col].map(normalize_string)
    )

    changed = both[changed_mask]

    return pd.DataFrame({
        "tag": changed[MERGED.TAG].values,
        "old_location": changed[asset_col].values,
        "new_location": changed[form_col].values,
    })


# ============================================================
# CUSTODIAN CHANGES
# ============================================================

def detect_custodian_changes(merged: pd.DataFrame) -> pd.DataFrame:

    both = _get_both_rows(merged)

    results = []

    for _, row in both.iterrows():

        asset_emp = normalize_string(
            row.get(MERGED.ASSET_EMP_ID)
        )

        form_emp = normalize_string(
            row.get(MERGED.FORM_EMP_ID)
        )

        if asset_emp != form_emp:

            results.append({
                MERGED.TAG: row.get(MERGED.TAG),

                "old_custodian_id":
                    row.get(MERGED.ASSET_EMP_ID),

                "new_custodian_id":
                    row.get(MERGED.FORM_EMP_ID),

                "old_custodian_name":
                    row.get(MERGED.ASSET_CUSTODIAN),

                "new_custodian_name":
                    row.get(MERGED.FORM_EMPLOYEE_NAME),
            })

    return pd.DataFrame(results)