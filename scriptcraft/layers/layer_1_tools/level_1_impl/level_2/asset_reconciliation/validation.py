import pandas as pd

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    require_columns,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    ASSET_REQUIRED_COLUMNS,
    FORM_REQUIRED_COLUMNS,
)


def validate_merge_inputs(asset_df: pd.DataFrame, form_df: pd.DataFrame):
    require_columns(asset_df, ASSET_REQUIRED_COLUMNS, "MERGE_ASSET_INPUT")
    require_columns(form_df, FORM_REQUIRED_COLUMNS, "MERGE_FORM_INPUT")
