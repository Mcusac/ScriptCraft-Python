# ============================================================
# orchestrator.py — PURE DAG ORCHESTRATOR
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    run_nodes,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    detect_missing,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    assert_merged,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    detect_form_duplicates,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_2 import (
    emit_input_debug,
    emit_merge_debug,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_3 import (
    DETECTORS,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_5 import (
    build_device_merged,
)



def run_comparison(
    asset_df: pd.DataFrame,
    form_df: pd.DataFrame,
    *,
    debug: bool = False,
) -> dict[str, pd.DataFrame]:
    """
    PURE ORCHESTRATION LAYER

    Responsibilities:
        - define execution order
        - delegate execution
        - collect outputs

    Does NOT:
        - know business rules
        - know detector logic
        - know schema structure
    """

    # STEP 1 — DEBUG INPUTS
    emit_input_debug(asset_df, form_df, enabled=debug)

    # STEP 2 — MERGE
    merged = build_device_merged(asset_df, form_df)

    assert_merged(merged)

    # STEP 3 — DEBUG MERGE
    emit_merge_debug(merged, enabled=debug)

    # STEP 4 — DETECTOR DAG EXECUTION (PURE)
    results = run_nodes(merged, DETECTORS)

    # STEP 5 — SPECIAL CASE DETECTORS (now normalized nodes would remove this later)
    missing_from_form, only_in_form = detect_missing(merged)

    results["missing_from_form"] = missing_from_form
    results["only_in_form"] = only_in_form
    results["duplicates_in_form"] = detect_form_duplicates(form_df)

    return results