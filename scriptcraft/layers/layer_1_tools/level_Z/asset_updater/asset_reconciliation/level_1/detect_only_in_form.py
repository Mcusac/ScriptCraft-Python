# ============================================================
# detect_only_in_form.py — flag-based detector
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import (
    MERGED,
)


def detect_only_in_form(merged: pd.DataFrame) -> pd.DataFrame:
    return merged[merged[MERGED.merge_flag] == "only_in_form"]