import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_2.key_semantics import (
    normalize_merge_key_value,
)


def normalize_merge_key(series: pd.Series) -> pd.Series:
    """
    Series-level transformation only.
    """

    return (
        series
        .map(normalize_merge_key_value)
        .replace("", pd.NA)
        .astype("string")
    )