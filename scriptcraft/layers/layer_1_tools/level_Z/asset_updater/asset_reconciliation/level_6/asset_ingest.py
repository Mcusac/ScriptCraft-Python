# ============================================================
# asset_ingest.py — asset normalization layer
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_5.asset_pipeline import (
    clean_asset_df,
)


def ingest_assets(asset_df_raw: pd.DataFrame) -> pd.DataFrame:
    return clean_asset_df(asset_df_raw)