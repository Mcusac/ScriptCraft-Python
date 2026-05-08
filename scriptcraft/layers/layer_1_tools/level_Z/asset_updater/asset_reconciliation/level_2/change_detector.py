# ============================================================
# detection/changes.py — schema-driven comparison detectors
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import (
    MERGED,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.text_canonicalizer import (
    canonical_text,
)


# ============================================================
# INTERNAL FILTER
# ============================================================

def _get_both_rows(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Restrict comparison space to matched records only.
    """

    return merged[
        merged[MERGED.merge_flag] == "both"
    ].copy()


# ============================================================
# LOCATION CHANGES
# ============================================================

def detect_location_changes(merged: pd.DataFrame) -> pd.DataFrame:

    both = _get_both_rows(merged)

    asset_col = MERGED.asset_location
    form_col = MERGED.form_location

    missing = {asset_col, form_col} - set(both.columns)

    if missing:
        raise RuntimeError(f"Missing merged columns: {missing}")

    changed_mask = (
        both[asset_col].map(canonical_text)
        != both[form_col].map(canonical_text)
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

    both = _get_both_rows(merged)

    results = []

    for _, row in both.iterrows():

        asset_emp = canonical_text(
            row.get(MERGED.asset_emp_id)
        )

        form_emp = canonical_text(
            row.get(MERGED.form_emp_id)
        )

        if asset_emp != form_emp:

            results.append({
                MERGED.tag: row.get(MERGED.tag),

                "old_custodian_id":
                    row.get(MERGED.asset_emp_id),

                "new_custodian_id":
                    row.get(MERGED.form_emp_id),

                "old_custodian_name":
                    row.get(MERGED.asset_custodian),

                "new_custodian_name":
                    row.get(MERGED.form_employee_name),
            })

    return pd.DataFrame(results)