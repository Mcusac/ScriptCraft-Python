# ============================================================
# utils/merge.py — schema-driven outer join (CLEAN CONTRACT)
# ============================================================

import pandas as pd

from layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import MERGED, ASSET_RAW, FORM_RAW


# ------------------------------------------------------------
# VALIDATION (POST-NORMALIZATION ONLY)
# ------------------------------------------------------------

def _validate_inputs(asset_df: pd.DataFrame, form_df: pd.DataFrame) -> None:
    """
    IMPORTANT:
    This runs AFTER normalization.
    """

    asset_required = [
        ASSET_RAW.tag,
        ASSET_RAW.emp_id,
        ASSET_RAW.location,
        ASSET_RAW.custodian,
        ASSET_RAW.description,
    ]

    form_required = [
        FORM_RAW.tag,
        FORM_RAW.emp_id,
        FORM_RAW.location,
        "employee_name",
    ]

    missing_asset = [c for c in asset_required if c not in asset_df.columns]
    missing_form = [c for c in form_required if c not in form_df.columns]

    if missing_asset:
        raise RuntimeError(f"Asset DF missing columns: {missing_asset}")

    if missing_form:
        raise RuntimeError(f"Form DF missing columns: {missing_form}")


# ------------------------------------------------------------
# INTERNAL NORMALIZATION GUARD (MERGE KEY SANITIZATION)
# ------------------------------------------------------------

def _normalize_merge_key(series: pd.Series) -> pd.Series:
    """
    Final defensive normalization layer BEFORE merge.

    This prevents:
    - string/int mismatches
    - whitespace issues
    - 'nan' string leaks
    """
    return (
        series.astype("string")
        .str.strip()
        .replace({"nan": pd.NA, "None": pd.NA})
    )


# ------------------------------------------------------------
# DEBUG / DIAGNOSTIC SNAPSHOT
# ------------------------------------------------------------

def _log_key_health(asset_df: pd.DataFrame, form_df: pd.DataFrame) -> None:
    """
    Lightweight diagnostics to catch join failures early.
    """

    print("\n--- MERGE KEY HEALTH CHECK ---")
    print(f"Asset tags null: {asset_df[ASSET_RAW.tag].isna().sum()}")
    print(f"Form tags null : {form_df[FORM_RAW.tag].isna().sum()}")

    print(f"Asset unique   : {asset_df[ASSET_RAW.tag].nunique()}")
    print(f"Form unique    : {form_df[FORM_RAW.tag].nunique()}")

    # sample overlap hint (cheap sanity check)
    asset_sample = set(asset_df[ASSET_RAW.tag].dropna().head(200))
    form_sample = set(form_df[FORM_RAW.tag].dropna().head(200))

    overlap = len(asset_sample.intersection(form_sample))
    print(f"Sample overlap : {overlap} (higher is better, <10 = problem)\n")


# ------------------------------------------------------------
# MERGE
# ------------------------------------------------------------

def build_device_merged(
    asset_df: pd.DataFrame,
    form_df: pd.DataFrame,
    *,
    debug: bool = False,
) -> pd.DataFrame:
    """
    Full outer merge producing MERGED schema contract.

    Assumes:
        - asset_df and form_df are already normalized
        - form_df already has employee_name
    """

    _validate_inputs(asset_df, form_df)

    asset_df = asset_df.copy()
    form_df = form_df.copy()

    # --------------------------------------------------------
    # CRITICAL FIX: enforce key normalization at merge boundary
    # --------------------------------------------------------

    asset_df[ASSET_RAW.tag] = _normalize_merge_key(asset_df[ASSET_RAW.tag])
    form_df[FORM_RAW.tag] = _normalize_merge_key(form_df[FORM_RAW.tag])

    # Drop empty keys (prevents garbage join rows)
    asset_df = asset_df[asset_df[ASSET_RAW.tag].notna()]
    form_df = form_df[form_df[FORM_RAW.tag].notna()]

    # --------------------------------------------------------
    # OPTIONAL DEBUG
    # --------------------------------------------------------

    if debug:
        _log_key_health(asset_df, form_df)

    # --------------------------------------------------------
    # RENAME → MERGED CONTRACT
    # --------------------------------------------------------

    asset_df = asset_df.rename(columns={
        ASSET_RAW.emp_id: MERGED.asset_emp_id,
        ASSET_RAW.location: MERGED.asset_location,
        ASSET_RAW.custodian: MERGED.asset_custodian,
        ASSET_RAW.description: MERGED.asset_description,
    })

    form_df = form_df.rename(columns={
        FORM_RAW.emp_id: MERGED.form_emp_id,
        FORM_RAW.location: MERGED.form_location,
        "employee_name": MERGED.form_employee_name,
    })

    # --------------------------------------------------------
    # MERGE (STABLE CONTRACT)
    # --------------------------------------------------------

    merged = pd.merge(
        asset_df,
        form_df,
        left_on=ASSET_RAW.tag,
        right_on=FORM_RAW.tag,
        how="outer",
        indicator=True,
        validate="many_to_many",  # catches accidental duplication explosions
    )

    print("\n--- MERGE DEBUG ---")
    print(merged["_merge"].value_counts())

    print("\nSample LEFT_ONLY:")
    print(
        merged[merged["_merge"] == "left_only"]
        [[ASSET_RAW.tag]]
        .head(10)
    )

    print("\nSample RIGHT_ONLY:")
    print(
        merged[merged["_merge"] == "right_only"]
        [[FORM_RAW.tag]]
        .head(10)
    )

    merged = merged.rename(columns={"_merge": MERGED.merge_flag})

    # --------------------------------------------------------
    # FINAL CONTRACT CHECK
    # --------------------------------------------------------

    required = [
        MERGED.tag,
        MERGED.asset_location,
        MERGED.form_location,
        MERGED.form_employee_name,
        MERGED.merge_flag,
    ]

    missing = [c for c in required if c not in merged.columns]

    if missing:
        raise RuntimeError(f"Merge contract failure. Missing columns: {missing}")

    return merged