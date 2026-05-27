from scriptcraft.layers.layer_0_core.level_0 import require_columns

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    ASSET_REQUIRED_COLUMNS,
    FORM_REQUIRED_COLUMNS,
)


def validate_merge_inputs(
    asset_df,
    form_df,
) -> None:
    require_columns(asset_df, ASSET_REQUIRED_COLUMNS, "MERGE_ASSET_INPUT")
    require_columns(form_df, FORM_REQUIRED_COLUMNS, "MERGE_FORM_INPUT")
