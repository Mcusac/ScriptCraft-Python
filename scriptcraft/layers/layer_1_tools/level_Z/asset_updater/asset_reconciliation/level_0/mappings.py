# ============================================================
# mappings.py — EXTERNAL CSV → RAW SCHEMA TRANSFORMATION
# ============================================================

import pandas as pd


# ============================================================
# ASSET CSV MAPPING
# ============================================================

ASSET_COLUMN_MAP = {
    "Tag Number": "tag",
    "ID": "emp_id",
    "Location": "location",
    "Custodian": "custodian",
    "Descr": "description",
}


# ============================================================
# FORM CSV BASE MAPPING (IMPORTANT: WIDE STRUCTURE HANDLED LATER)
# ============================================================

FORM_BASE_COLUMN_MAP = {
    "Employee ID": "emp_id",
    "First Name": "first_name",
    "Last Name": "last_name",
}


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