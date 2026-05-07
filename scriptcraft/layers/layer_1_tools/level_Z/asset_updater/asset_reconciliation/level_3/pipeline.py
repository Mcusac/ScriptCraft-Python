import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import (
    ASSET_RAW_TAG,
    FORM_RAW_TAG,
    MERGED_TAG,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.merge_engine import execute_merge
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.key_normalizer import prepare_merge_keys
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_2.validation import validate_merge_inputs
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_2.transforms import rename_asset_columns, rename_form_columns, project_final_tag


def build_device_merged(asset_df: pd.DataFrame, form_df: pd.DataFrame) -> pd.DataFrame:
    """
    DAG ORCHESTRATION

    validate → normalize keys → rename → merge → finalize
    """

    validate_merge_inputs(asset_df, form_df)

    asset_df, form_df = prepare_merge_keys(asset_df, form_df)

    asset_df = rename_asset_columns(asset_df)
    form_df = rename_form_columns(form_df)

    merged = execute_merge(
        asset_df,
        form_df,
        left_key=ASSET_RAW_TAG,
        right_key=FORM_RAW_TAG,
    )

    merged = project_final_tag(merged, ASSET_RAW_TAG, MERGED_TAG)

    return merged