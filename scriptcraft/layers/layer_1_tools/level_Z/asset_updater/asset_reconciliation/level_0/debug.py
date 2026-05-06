# ============================================================
# utils/debug.py — optional diagnostic helpers
# Imported only when debug=True; no side effects otherwise.
# ============================================================

import pandas as pd


def debug_raw_inputs(
    asset_df: pd.DataFrame,
    form_df: pd.DataFrame,
    tag_col: str,
) -> None:
    print("\n--- DEBUG: RAW INPUT ---")
    print(f"Asset rows : {len(asset_df)}")
    print(f"Form rows  : {len(form_df)}")
    if "Device Tag" in form_df.columns:
        print(f"Unique form tags  : {form_df['Device Tag'].nunique()}")
    print(f"Unique asset tags : {asset_df[tag_col].nunique()}")


def debug_merge(merged: pd.DataFrame, asset_tag_col: str) -> None:
    print("\n--- DEBUG: MERGE RESULTS ---")
    if "_merge" not in merged.columns:
        print("⚠️  No _merge column found")
        return

    print(merged["_merge"].value_counts())

    cols = [c for c in [asset_tag_col, "Device Tag", "_merge"] if c in merged.columns]
    print("\nSample merged rows:")
    print(merged[cols].head(10))