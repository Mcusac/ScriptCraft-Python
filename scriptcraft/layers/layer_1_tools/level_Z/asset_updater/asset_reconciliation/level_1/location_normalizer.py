# ============================================================
# normalizer/location.py — location-string cleaning pipeline
#
# Pure functions; schema-aware; deterministic.
# ============================================================

import pandas as pd

from layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import OFF_CAMPUS_CANONICAL


# -----------------------------
# STEP 0 — WHITESPACE NORMALIZATION
# -----------------------------

def normalize_whitespace(series: pd.Series) -> pd.Series:
    return (
        series
        .astype("string")  # safer than str (preserves <NA>)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


# -----------------------------
# STEP 1 — BUILDING NORMALIZATION
# -----------------------------

def normalize_building_codes(series: pd.Series) -> pd.Series:
    return (
        series
        .astype("string")
        .str.upper()
        .str.replace(r"\bHP\b", "PCC", regex=True)
    )


# -----------------------------
# STEP 2 — REMOVE NOISE
# -----------------------------

def strip_room_noise(series: pd.Series) -> pd.Series:
    return (
        series
        .astype("string")
        .str.replace(r"(?i)\broom\b", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


# -----------------------------
# STEP 3 — REMOVE HYPHENS
# -----------------------------

def remove_hyphens(series: pd.Series) -> pd.Series:
    return series.astype("string").str.replace("-", "", regex=False)


# -----------------------------
# STEP 4 — SPACING NORMALIZATION
# -----------------------------

def enforce_spacing(series: pd.Series) -> pd.Series:
    return series.astype("string").str.replace(
        r"([A-Z]+)\s*([0-9]{3,})",
        r"\1  \2",
        regex=True,
    )


# -----------------------------
# STEP 5 — OFF-CAMPUS NORMALIZATION (schema-driven)
# -----------------------------

def normalize_off_campus(series: pd.Series) -> pd.Series:
    """
    Normalize any off-campus variant to canonical schema value.
    """
    series = series.astype("string")

    mask = series.str.contains(r"(?i)\boff\s*campus\b", na=False)
    series.loc[mask] = OFF_CAMPUS_CANONICAL

    return series


# -----------------------------
# STEP 6 — STRUCTURAL PARSING
# -----------------------------

def extract_location_parts(series: pd.Series) -> pd.DataFrame:
    return series.str.extract(
        r"(?P<building>[A-Z]+)[\s\-]*?(?P<room>[0-9]+[A-Z]*)",
        expand=True,
    )


def rebuild_location(parts: pd.DataFrame) -> pd.Series:
    return parts.apply(
        lambda x: f"{x['building']}  {x['room']}"
        if pd.notna(x["building"]) and pd.notna(x["room"])
        else pd.NA,
        axis=1,
    )


# -----------------------------
# PIPELINE ORCHESTRATOR
# -----------------------------

def normalize_location(series: pd.Series) -> pd.Series:
    """
    Full deterministic normalization pipeline.

    Order is intentional and preserved.
    """

    # Preserve true missing values correctly
    na_mask = series.isna()

    series = normalize_whitespace(series)
    series = normalize_building_codes(series)
    series = strip_room_noise(series)
    series = remove_hyphens(series)
    series = normalize_off_campus(series)
    series = enforce_spacing(series)

    parts = extract_location_parts(series)
    series = rebuild_location(parts)

    # restore missing values safely
    series.loc[na_mask] = pd.NA

    return series