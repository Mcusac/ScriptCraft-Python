import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_1.contracts import ASSET_TO_MERGED_MAP, FORM_TO_MERGED_MAP


def rename_asset_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=ASSET_TO_MERGED_MAP)


def rename_form_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=FORM_TO_MERGED_MAP)


def project_final_tag(df: pd.DataFrame, raw_tag: str, merged_tag: str):
    """
    Ensures DAG-safe final contract alignment.
    """
    if raw_tag in df.columns:
        return df.rename(columns={raw_tag: merged_tag})
    return df