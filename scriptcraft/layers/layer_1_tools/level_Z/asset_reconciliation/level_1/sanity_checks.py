# ============================================================
# sanity_checks.py — runner debug instrumentation
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_0.schema import (
    ASSET_RAW,
    FORM_RAW,
)


def run_sanity_checks(
    asset_df: pd.DataFrame,
    form_df: pd.DataFrame,
) -> None:

    print("\n--- RUNNER DEBUG (POST-NORMALIZATION) ---")

    print(f"Form rows: {len(form_df)}")
    print(f"Asset rows: {len(asset_df)}")

    print("\nForm tag sample:")
    print(form_df[FORM_RAW.tag].head(10).tolist())

    print("\nAsset tag sample:")
    print(asset_df[ASSET_RAW.tag].head(10).tolist())

    print("\nOverlap estimate:")

    asset_set = set(
        asset_df[ASSET_RAW.tag]
        .dropna()
        .astype(str)
    )

    form_set = set(
        form_df[FORM_RAW.tag]
        .dropna()
        .astype(str)
    )

    print(len(asset_set.intersection(form_set)))