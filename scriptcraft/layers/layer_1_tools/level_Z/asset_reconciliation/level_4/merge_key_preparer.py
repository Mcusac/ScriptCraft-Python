import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.contracts import (
    ASSET_REQUIRED_COLUMNS,
    FORM_REQUIRED_COLUMNS,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_3.key_normalizer import (
    normalize_merge_key,
)


def prepare_merge_keys(asset_df: pd.DataFrame, form_df: pd.DataFrame):
    """
    DAG stage: schema-safe merge key preparation.
    """

    asset_df = asset_df.copy()
    form_df = form_df.copy()

    # --------------------------------------------------------
    # primary key column (positional safety layer)
    # --------------------------------------------------------

    asset_df.iloc[:, 0] = normalize_merge_key(asset_df.iloc[:, 0])
    form_df.iloc[:, 0] = normalize_merge_key(form_df.iloc[:, 0])

    # --------------------------------------------------------
    # contract-based explicit keys (source of truth)
    # --------------------------------------------------------

    asset_key = ASSET_REQUIRED_COLUMNS[0]
    form_key = FORM_REQUIRED_COLUMNS[0]

    asset_df[asset_key] = normalize_merge_key(asset_df[asset_key])
    form_df[form_key] = normalize_merge_key(form_df[form_key])

    # --------------------------------------------------------
    # filter invalid keys (DAG boundary enforcement)
    # --------------------------------------------------------

    asset_df = asset_df[asset_df[asset_key].notna()]
    form_df = form_df[form_df[form_key].notna()]

    return asset_df, form_df