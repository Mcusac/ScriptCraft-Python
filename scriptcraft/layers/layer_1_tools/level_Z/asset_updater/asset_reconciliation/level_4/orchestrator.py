# ============================================================
# orchestrator.py — comparison DAG (clean orchestration layer)
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import MERGED, OFF_CAMPUS_CANONICAL
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.debug_print import debug_raw_inputs, debug_merge
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.detection.missing import detect_missing
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.detection.changes import detect_location_changes, detect_custodian_changes
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.detection.duplicates import detect_form_duplicates
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_3.pipeline import build_device_merged


# ------------------------------------------------------------
# SAFE FILTER (kept minimal, no business logic)
# ------------------------------------------------------------

def _safe_eq(df: pd.DataFrame, col: str, value: str) -> pd.Series:
    """
    Null-safe equality check for filtering only.
    """
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    return df[col].astype("string").eq(value)


# ------------------------------------------------------------
# ORCHESTRATION DAG
# ------------------------------------------------------------

def run_comparison(
    asset_df: pd.DataFrame,
    form_df: pd.DataFrame,
    *,
    debug: bool = False,
) -> dict[str, pd.DataFrame]:
    """
    Executes full reconciliation pipeline.

    Responsibilities:
        - call merge
        - call detectors
        - return results

    Does NOT:
        - transform data
        - validate schema
        - implement business rules
    """

    # --------------------------------------------------------
    # STEP 1 — DEBUG INPUTS
    # --------------------------------------------------------
    if debug:
        debug_raw_inputs(asset_df, form_df, MERGED.tag)

    # --------------------------------------------------------
    # STEP 2 — DUPLICATE DETECTION (pre-merge)
    # --------------------------------------------------------
    duplicate_results = detect_form_duplicates(form_df)

    # --------------------------------------------------------
    # STEP 3 — MERGE
    # --------------------------------------------------------
    merged = build_device_merged(asset_df, form_df)

    if MERGED.merge_flag not in merged.columns:
        raise RuntimeError("Merge contract violation: missing merge_flag")

    # --------------------------------------------------------
    # STEP 4 — DEBUG MERGED OUTPUT
    # --------------------------------------------------------
    if debug:
        debug_merge(merged, MERGED.tag)

    # --------------------------------------------------------
    # STEP 5 — DETECTORS (pure functions)
    # --------------------------------------------------------
    missing_from_form, only_in_form = detect_missing(merged)
    location_changes = detect_location_changes(merged)
    custodian_changes = detect_custodian_changes(merged)

    # --------------------------------------------------------
    # STEP 6 — OFF-CAMPUS FILTER (simple orchestration filter only)
    # --------------------------------------------------------
    asset_off = _safe_eq(
        merged,
        MERGED.asset_location,
        OFF_CAMPUS_CANONICAL,
    )

    form_off = _safe_eq(
        merged,
        MERGED.form_location,
        OFF_CAMPUS_CANONICAL,
    )

    off_campus = merged.loc[
        asset_off | form_off,
        [
            MERGED.tag,
            MERGED.asset_location,
            MERGED.form_location,
            MERGED.merge_flag,
        ],
    ].copy()
    
    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------
    return {
        "missing_from_form": missing_from_form,
        "only_in_form": only_in_form,
        "location_changes": location_changes,
        "custodian_changes": custodian_changes,
        "duplicate_results": duplicate_results,
        "off_campus": off_campus,
    }