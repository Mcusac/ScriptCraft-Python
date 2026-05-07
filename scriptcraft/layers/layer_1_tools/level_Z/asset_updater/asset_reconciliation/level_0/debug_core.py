# level_0/debug.py

import pandas as pd


def debug_raw_inputs(asset_df: pd.DataFrame, form_df: pd.DataFrame, tag_col: str) -> None:
    print("\n--- DEBUG: RAW INPUT ---")
    print(f"Asset rows : {len(asset_df)}")
    print(f"Form rows  : {len(form_df)}")

    if tag_col in form_df.columns:
        print(f"Unique form tags  : {form_df[tag_col].nunique()}")

    if tag_col in asset_df.columns:
        print(f"Unique asset tags : {asset_df[tag_col].nunique()}")


def debug_merge(merged: pd.DataFrame, tag_col: str, merge_col: str = "_merge") -> None:
    print("\n--- DEBUG: MERGE RESULTS ---")

    if merge_col not in merged.columns:
        print("⚠️ Missing merge column")
        return

    print(merged[merge_col].value_counts())

    cols = [c for c in [tag_col, merge_col] if c in merged.columns]

    print("\nSample rows:")
    print(merged[cols].head(10))