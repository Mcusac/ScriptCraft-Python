# ============================================================
# detection/changes.py — schema-driven comparison detectors
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import MERGED


# ------------------------------------------------------------
# INTERNAL HELPER
# ------------------------------------------------------------

def _norm_str(val) -> str:
    """Normalize values for comparison."""
    if val is None or pd.isna(val):
        return ""
    s = str(val).strip().lower()
    return "" if s in ("nan", "none", "na") else s


# ============================================================
# LOCATION CHANGES
# ============================================================

def detect_location_changes(merged: pd.DataFrame) -> pd.DataFrame:

    both = merged[merged[MERGED.merge_flag] == "both"].copy()

    asset_col = MERGED.asset_location
    form_col = MERGED.form_location

    missing = {asset_col, form_col} - set(both.columns)
    if missing:
        raise RuntimeError(f"Missing merged columns: {missing}")

    changed_mask = (
        both[asset_col].apply(_norm_str)
        != both[form_col].apply(_norm_str)
    )

    changed = both[changed_mask]

    return pd.DataFrame({
        "tag": changed[MERGED.tag].values,
        "old_location": changed[asset_col].values,
        "new_location": changed[form_col].values,
    })


# ============================================================
# CUSTODIAN CHANGES
# ============================================================

def detect_custodian_changes(merged: pd.DataFrame) -> pd.DataFrame:

    both = merged[merged[MERGED.merge_flag] == "both"].copy()

    results = []

    for _, row in both.iterrows():

        asset_emp = _norm_str(row.get(MERGED.asset_emp_id))
        form_emp = _norm_str(row.get(MERGED.form_emp_id))

        if asset_emp != form_emp:
            results.append({
                MERGED.tag: row.get(MERGED.tag),

                "old_custodian_id": row.get(MERGED.asset_emp_id),
                "new_custodian_id": row.get(MERGED.form_emp_id),

                "old_custodian_name": row.get(MERGED.asset_custodian),
                "new_custodian_name": row.get(MERGED.form_employee_name),
            })

    return pd.DataFrame(results)