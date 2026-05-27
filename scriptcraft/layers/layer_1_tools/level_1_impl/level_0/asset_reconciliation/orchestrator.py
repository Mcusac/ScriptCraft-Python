# ============================================================
# orchestrator.py — PURE DAG ORCHESTRATOR
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_0_core.level_0 import run_nodes

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    assert_merged,
    detect_form_duplicates,
    detect_missing,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    emit_input_debug,
    emit_merge_debug,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    MERGED_DETECTORS,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    build_device_merged,
)


def run_asset_form_comparison(
    asset_df: pd.DataFrame,
    form_df: pd.DataFrame,
    *,
    debug: bool = False,
) -> dict[str, pd.DataFrame]:
    """
    Pure orchestration: merge → merged detectors → form-side detectors.

    Merged-table detectors run through ``run_nodes``. Detectors that need
    the raw form frame or return multiple named outputs stay explicit below.
    """
    emit_input_debug(asset_df, form_df, enabled=debug)

    merged = build_device_merged(asset_df, form_df)
    assert_merged(merged)
    emit_merge_debug(merged, enabled=debug)

    results = run_nodes(merged, MERGED_DETECTORS)

    missing_from_form, only_in_form = detect_missing(merged)
    results["missing_from_form"] = missing_from_form
    results["only_in_form"] = only_in_form
    results["duplicates_in_form"] = detect_form_duplicates(form_df)

    return results
