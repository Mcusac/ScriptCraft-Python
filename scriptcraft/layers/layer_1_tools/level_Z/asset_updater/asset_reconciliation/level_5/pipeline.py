import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.merge_engine import (
    execute_merge,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import (
    ASSET_RAW,
    FORM_RAW,
    MERGED,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_2.validation import (
    validate_merge_inputs,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_2.transforms import (
    rename_asset_columns,
    rename_form_columns,
    project_final_tag,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_4.merge_key_preparer import (
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
    rename
        ↓
    merge
        ↓
    finalize
    """

    # --------------------------------------------------------
    # STEP 1 — VALIDATE
    # --------------------------------------------------------

    validate_merge_inputs(
        asset_df,
        form_df,
    )

    # --------------------------------------------------------
    # STEP 2 — NORMALIZE MERGE KEYS
    # --------------------------------------------------------

    asset_df, form_df = prepare_merge_keys(
        asset_df,
        form_df,
    )

    # --------------------------------------------------------
    # STEP 3 — RENAME TO MERGED CONTRACT
    # --------------------------------------------------------

    asset_df = rename_asset_columns(asset_df)

    form_df = rename_form_columns(form_df)


    print("\n--- POST VALIDATE ---")
    print(form_df.columns.tolist())

    print("\n--- POST KEY NORMALIZE ---")
    print(form_df.columns.tolist())

    print("\n--- POST FORM RENAME ---")
    print(form_df.columns.tolist())

    if "location" in form_df.columns:
        print(form_df[["tag", "location"]].head())

    if "form_location" in form_df.columns:
        print(form_df[["tag", "form_location"]].head())


    # --------------------------------------------------------
    # STEP 4 — MERGE
    # --------------------------------------------------------

    target_tags = ["00037435", "00040524"]

    print(
        form_df[
            form_df["tag"].isin(target_tags)
        ][["tag", "form_location"]]
    )

    merged = execute_merge(
        asset_df,
        form_df,
        left_key=ASSET_RAW.tag,
        right_key=FORM_RAW.tag,
    )


    print(
        merged[
            merged["tag"].isin(target_tags)
        ][[
            "tag",
            "asset_location",
            "form_location",
        ]]
    )

    # --------------------------------------------------------
    # STEP 5 — FINALIZE TAG CONTRACT
    # --------------------------------------------------------

    merged = project_final_tag(
        merged,
        ASSET_RAW.tag,
        MERGED.tag,
    )

    return merged