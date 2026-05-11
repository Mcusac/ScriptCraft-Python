import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_1.contracts import ASSET_REQUIRED_COLUMNS, FORM_REQUIRED_COLUMNS


def require_columns(df: pd.DataFrame, required: list[str], context: str = ""):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(f"[SCHEMA ERROR] Missing columns in {context}: {missing}")


def validate_merge_inputs(asset_df: pd.DataFrame, form_df: pd.DataFrame):
    require_columns(asset_df, ASSET_REQUIRED_COLUMNS, "MERGE_ASSET_INPUT")
    require_columns(form_df, FORM_REQUIRED_COLUMNS, "MERGE_FORM_INPUT")