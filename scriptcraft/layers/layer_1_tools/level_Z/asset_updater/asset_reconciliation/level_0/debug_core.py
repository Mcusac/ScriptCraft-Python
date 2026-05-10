import pandas as pd


def get_dataframe_summary(df: pd.DataFrame, key_col: str | None = None) -> dict:
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "unique_keys": df[key_col].nunique() if key_col and key_col in df.columns else None,
        "null_counts": df.isna().sum().to_dict(),
    }


def get_merge_summary(df: pd.DataFrame, merge_col: str = "_merge") -> dict:
    if merge_col not in df.columns:
        return {"error": "missing_merge_column"}

    return {
        "distribution": df[merge_col].value_counts().to_dict(),
        "sample": df[[merge_col]].head(10).to_dict(orient="records"),
    }