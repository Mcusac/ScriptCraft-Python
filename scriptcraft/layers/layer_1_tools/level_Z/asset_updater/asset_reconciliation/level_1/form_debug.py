# ============================================================
# form_debug.py — diagnostics only (NOT part of DAG)
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import FORM_RAW


def debug_form(df: pd.DataFrame) -> None:
    print("\n--- FORM DEBUG ---")
    print(f"Rows: {len(df)}")
    print(f"Unique tags: {df[FORM_RAW.tag].nunique()}")
    print(f"Null tags: {df[FORM_RAW.tag].isna().sum()}")
    print(f"Null locations: {df[FORM_RAW.location].isna().sum()}")
    print(f"Null emp_ids: {df[FORM_RAW.emp_id].isna().sum()}")