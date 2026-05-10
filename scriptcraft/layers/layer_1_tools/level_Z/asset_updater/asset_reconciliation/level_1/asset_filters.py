import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.constants import (
    ASSET_DESCRIPTION_PREFIX,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import (
    ASSET_RAW,
)


def filter_computers_only(df: pd.DataFrame) -> pd.DataFrame:
    desc = ASSET_RAW.description

    if desc not in df.columns:
        return df

    mask = df[desc].astype("string").str.lower().str.startswith(
        ASSET_DESCRIPTION_PREFIX
    )

    return df[mask].copy()