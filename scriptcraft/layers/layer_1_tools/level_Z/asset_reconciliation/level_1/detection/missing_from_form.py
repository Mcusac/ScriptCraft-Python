# ============================================================
# detect_missing_from_form.py — flag-based detector
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_0.schema import (
    MERGED,
)


def detect_missing_from_form(merged: pd.DataFrame) -> pd.DataFrame:
    """Assets present in the asset database but absent from the form."""
    return merged[merged[MERGED.merge_flag] == "left_only"]