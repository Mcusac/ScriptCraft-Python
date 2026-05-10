# ============================================================
# orchestrator.py — PURE DAG ORCHESTRATOR
# ============================================================

import pandas as pd

<<<<<<< HEAD
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.detection.missing_from_form import (
    detect_missing_from_form,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.detection.only_in_form import (
=======
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.detect_missing_from_form import (
    detect_missing_from_form,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.detect_only_in_form import (
>>>>>>> 182d6be043d82fdc23c5fc4c567ad4e195b94c00
    detect_only_in_form,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.dag_runner import (
    run_nodes,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.merge_contracts import (
    validate_merged_contract,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_2.debug_hooks import (
    emit_input_debug,
    emit_merge_debug,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_3.registry import (
    DETECTORS,
)
<<<<<<< HEAD
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_5.merge_pipeline import (
=======
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_5.pipeline import (
>>>>>>> 182d6be043d82fdc23c5fc4c567ad4e195b94c00
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

    validate_merged_contract(merged)

    # STEP 3 — DEBUG MERGE
    emit_merge_debug(merged, enabled=debug)

    # STEP 4 — DETECTOR DAG EXECUTION (PURE)
    results = run_nodes(merged, DETECTORS)

    # STEP 5 — SPECIAL CASE DETECTORS (now normalized nodes would remove this later)
    results["missing_from_form"] = detect_missing_from_form(merged)
    results["only_in_form"] = detect_only_in_form(merged)

    return results