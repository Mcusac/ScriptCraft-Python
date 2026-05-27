# ============================================================
# debug/hooks.py — debug orchestration hooks
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    MERGED,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    debug_merge,
    debug_raw_inputs,
)


def emit_input_debug(asset_df, form_df, *, enabled: bool):
    if enabled:
        debug_raw_inputs(asset_df, form_df, MERGED.tag)


def emit_merge_debug(merged: pd.DataFrame, *, enabled: bool):
    if enabled:
        debug_merge(merged, MERGED.tag)