import pandas as pd

# ============================================================
# STANDARDIZATION FUNCTION (INGESTION ONLY)
# ============================================================

def standardize_columns(df: pd.DataFrame, column_map: dict) -> pd.DataFrame:
    """
    External CSV → RAW schema.
    Must be first operation in DAG.
    """

    missing = [c for c in column_map.keys() if c not in df.columns]
    if missing:
        raise RuntimeError(f"[SCHEMA ERROR] Missing raw columns: {missing}")

    return df.rename(columns=column_map)