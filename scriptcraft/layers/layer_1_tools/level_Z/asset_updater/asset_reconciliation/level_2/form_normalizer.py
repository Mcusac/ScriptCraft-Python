# ============================================================
# normalizer/form.py — form flattening + normalization (v3)
# WIDE → LONG FIRST PRINCIPLE
# ============================================================

import pandas as pd

from layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import (
    FORM_RAW,
    FORM_COLUMN_MAP,
    standardize_columns,
)
from layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.tag_normalizer import normalize_tag, normalize_employee_id
from layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.location_normalizer import normalize_location


# ------------------------------------------------------------
# CONFIGURATION (fixed contract, not dynamic inference)
# ------------------------------------------------------------

MAX_DEVICE_SLOTS = 5  # known business rule


# ------------------------------------------------------------
# SAFE ACCESSOR
# ------------------------------------------------------------

def _safe_get(row, col):
    if col not in row.index:
        return None
    return row.get(col)


# ------------------------------------------------------------
# FULL NAME BUILDER
# ------------------------------------------------------------

def _build_full_name(row) -> str:
    first = str(_safe_get(row, FORM_RAW.first_name) or "").strip()
    last = str(_safe_get(row, FORM_RAW.last_name) or "").strip()
    return f"{first} {last}".strip()


# ------------------------------------------------------------
# WIDE → LONG TRANSFORMATION (CORE FIX)
# ------------------------------------------------------------

def _reshape_form_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts wide form structure:

        Device Tag, Device Tag1, Device Tag2...
        Location..., Location1, Location2...

    INTO:

        tag | emp_id | location | employee_name
    """

    records = []

    for _, row in df.iterrows():

        employee_name = _build_full_name(row)
        emp_id = _safe_get(row, FORM_RAW.emp_id)

        for i in range(MAX_DEVICE_SLOTS):

            suffix = "" if i == 0 else str(i)

            tag_col = f"Device Tag{suffix}"
            loc_col = f"Location of Device (ie HP 505 or Off Campus){suffix}"

            tag = _safe_get(row, tag_col)
            location = _safe_get(row, loc_col)

            # ----------------------------------------------------
            # STRICT FILTER (only real assignments)
            # ----------------------------------------------------
            if tag is None or pd.isna(tag):
                continue

            if str(tag).strip() == "":
                continue

            records.append({
                FORM_RAW.tag: tag,
                FORM_RAW.emp_id: emp_id,
                FORM_RAW.location: location,
                "employee_name": employee_name,
            })

    return pd.DataFrame(records)


# ------------------------------------------------------------
# NORMALIZATION PIPELINE
# ------------------------------------------------------------

def normalize_form(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline:

    1. Standardize columns
    2. Reshape wide → long (CRITICAL STEP)
    3. Normalize values
    4. Debug output
    """

    # --------------------------------------------------------
    # STEP 1 — INGESTION NORMALIZATION
    # --------------------------------------------------------
    df = standardize_columns(df.copy(), FORM_COLUMN_MAP)

    # --------------------------------------------------------
    # STEP 2 — STRUCTURAL TRANSFORMATION (FIXED)
    # --------------------------------------------------------
    df_out = _reshape_form_wide_to_long(df)

    if df_out.empty:
        print("\n--- FORM NORMALIZATION DEBUG ---")
        print("No records produced after reshape")
        return df_out

    # --------------------------------------------------------
    # STEP 3 — VALUE NORMALIZATION
    # --------------------------------------------------------
    df_out[FORM_RAW.tag] = normalize_tag(df_out[FORM_RAW.tag])
    df_out[FORM_RAW.emp_id] = normalize_employee_id(df_out[FORM_RAW.emp_id])
    df_out[FORM_RAW.location] = normalize_location(df_out[FORM_RAW.location])

    # --------------------------------------------------------
    # STEP 4 — DEBUG OUTPUT (single source of truth)
    # --------------------------------------------------------
    print("\n--- FORM NORMALIZATION DEBUG ---")
    print(f"Rows produced: {len(df_out)}")
    print(f"Unique tags  : {df_out[FORM_RAW.tag].nunique()}")

    print("\nSample tags:")
    print(df_out[FORM_RAW.tag].head(10).tolist())

    print("\nNull tags:")
    print(df_out[FORM_RAW.tag].isna().sum())

    print("\nNull locations:")
    print(df_out[FORM_RAW.location].isna().sum())

    print("\nNull emp_ids:")
    print(df_out[FORM_RAW.emp_id].isna().sum())

    return df_out