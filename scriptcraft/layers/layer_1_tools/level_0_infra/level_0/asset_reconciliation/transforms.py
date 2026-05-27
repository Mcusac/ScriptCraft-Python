import pandas as pd


def project_final_tag(df: pd.DataFrame, raw_tag: str, merged_tag: str):
    """
    Ensures DAG-safe final contract alignment.
    """
    if raw_tag in df.columns:
        return df.rename(columns={raw_tag: merged_tag})
    return df
