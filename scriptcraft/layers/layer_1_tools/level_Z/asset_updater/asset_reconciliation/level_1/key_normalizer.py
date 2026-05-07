import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.tag_normalizer import (
    sanitize,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.contracts import ASSET_REQUIRED_COLUMNS, FORM_REQUIRED_COLUMNS


def normalize_merge_key(series: pd.Series) -> pd.Series:
    """
    Boundary-safe merge key normalization.
    """

    normalized = series.map(sanitize)
    normalized = normalized.replace("", pd.NA)

    return normalized.astype("string")


def prepare_merge_keys(asset_df: pd.DataFrame, form_df: pd.DataFrame):
    """
    DAG stage: normalize + clean join keys.
    """

    asset_df = asset_df.copy()
    form_df = form_df.copy()

    asset_df[asset_df.columns[0]]  # ensures dataframe touch safety (optional guard)

    asset_df.iloc[:, 0] = normalize_merge_key(asset_df.iloc[:, 0])
    form_df.iloc[:, 0] = normalize_merge_key(form_df.iloc[:, 0])

    # explicit key usage (better than positional if available)
    asset_df[ASSET_REQUIRED_COLUMNS[0]] = normalize_merge_key(
        asset_df[ASSET_REQUIRED_COLUMNS[0]]
    )

    form_df[FORM_REQUIRED_COLUMNS[0]] = normalize_merge_key(
        form_df[FORM_REQUIRED_COLUMNS[0]]
    )

    asset_df = asset_df[asset_df[ASSET_REQUIRED_COLUMNS[0]].notna()]
    form_df = form_df[form_df[FORM_REQUIRED_COLUMNS[0]].notna()]

    return asset_df, form_df