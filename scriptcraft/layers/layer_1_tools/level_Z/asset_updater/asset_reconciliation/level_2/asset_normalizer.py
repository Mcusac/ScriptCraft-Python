# ============================================================
# normalizer/asset.py — asset-database cleaning
# ============================================================

import pandas as pd

from layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import (
    ASSET_RAW,
    ASSET_COLUMN_MAP,
    standardize_columns,
    ASSET_DESCRIPTION_PREFIX,
)
from layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.tag_normalizer import normalize_tag, normalize_employee_id
from layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.location_normalizer import normalize_location


# ------------------------------------------------------------
# DOMAIN FILTER
# ------------------------------------------------------------

def filter_computers_only(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep only rows whose description matches asset domain rule.
    """

    desc_col = ASSET_RAW.description

    if desc_col not in df.columns:
        return df

    mask = (
        df[desc_col]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.startswith(ASSET_DESCRIPTION_PREFIX)
    )

    return df[mask].copy()


# ------------------------------------------------------------
# FULL NORMALIZATION PIPELINE
# ------------------------------------------------------------

def clean_asset_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Asset normalization pipeline:

      1. Convert CSV → canonical schema
      2. Filter domain assets
      3. Normalize fields
      4. Clean custodians
    """

    df = df.copy()

    # ========================================================
    # STEP 1 — CRITICAL FIX (was missing entirely)
    # ========================================================
    df = standardize_columns(df, ASSET_COLUMN_MAP)

    # ========================================================
    # STEP 2 — domain filtering
    # ========================================================
    df = filter_computers_only(df)

    # ========================================================
    # STEP 3 — normalization
    # ========================================================
    df[ASSET_RAW.tag] = normalize_tag(df[ASSET_RAW.tag])
    df[ASSET_RAW.emp_id] = normalize_employee_id(df[ASSET_RAW.emp_id])
    df[ASSET_RAW.location] = normalize_location(df[ASSET_RAW.location])

    # ========================================================
    # STEP 4 — custodian cleanup
    # ========================================================
    cust = ASSET_RAW.custodian
    if cust in df.columns:
        df[cust] = df[cust].astype(str).str.strip()

    return df