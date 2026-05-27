# ============================================================
# merge_pipeline.py — merge DAG orchestrator
# ============================================================
import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    outer_merge_with_indicator,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    ASSET_RAW,
    FORM_RAW,
    MERGED,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    project_final_tag,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    ASSET_TO_MERGED_MAP,
    FORM_TO_MERGED_MAP,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    validate_merge_inputs,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    prepare_merge_keys,
)

# ============================================================
# MERGE DAG
# ============================================================

def build_device_merged(
    asset_df: pd.DataFrame,
    form_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    DAG ORCHESTRATION

    validate
        ↓
    normalize keys
        ↓
    rename to merged contract
        ↓
    merge
        ↓
    finalize tag contract
    """

    # STEP 1 — VALIDATE
    validate_merge_inputs(asset_df, form_df)

    # STEP 2 — NORMALIZE MERGE KEYS
    asset_df, form_df = prepare_merge_keys(asset_df, form_df)

    # STEP 3 — RENAME TO MERGED CONTRACT
    asset_df = asset_df.rename(columns=ASSET_TO_MERGED_MAP)
    form_df = form_df.rename(columns=FORM_TO_MERGED_MAP)

    # STEP 4 — MERGE
    merged = outer_merge_with_indicator(
        asset_df,
        form_df,
        left_on=ASSET_RAW.tag,
        right_on=FORM_RAW.tag,
        indicator_col="merge_flag",
    )

    # STEP 5 — FINALIZE TAG CONTRACT
    merged = project_final_tag(
        merged,
        ASSET_RAW.tag,
        MERGED.tag,
    )

    return merged