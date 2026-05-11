import pandas as pd


def execute_merge(asset_df: pd.DataFrame, form_df: pd.DataFrame, *, left_key: str, right_key: str):
    merged = pd.merge(
        asset_df,
        form_df,
        left_on=left_key,
        right_on=right_key,
        how="outer",
        indicator=True,
        validate="many_to_many",
    )

    return merged.rename(columns={"_merge": "merge_flag"})