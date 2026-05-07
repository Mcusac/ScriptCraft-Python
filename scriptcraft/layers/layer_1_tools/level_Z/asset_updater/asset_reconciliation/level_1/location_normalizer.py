# ============================================================
# location_normalizer.py — canonical location normalization
#
# DESIGN:
# - Pure transformation pipeline
# - Explicit DAG execution order
# - Reusable normalization primitives
# - Business rules isolated
# - Missing-value preservation guaranteed
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.constants import (
    OFF_CAMPUS_CANONICAL,
)


# ============================================================
# CONSTANTS
# ============================================================

_STRING_DTYPE = "string"

_WHITESPACE_REGEX = r"\s+"

_ROOM_REGEX = r"(?i)\broom\b"

_BUILDING_REGEX = r"\bHP\b"

_SPACING_REGEX = r"([A-Z]+)\s*([0-9]{3,})"


# ============================================================
# CORE STRING OPERATIONS
# ============================================================

def _to_string_dtype(series: pd.Series) -> pd.Series:
    """
    Safe string conversion preserving <NA>.
    """

    return series.astype(_STRING_DTYPE)


def _collapse_whitespace(series: pd.Series) -> pd.Series:
    """
    Normalizes repeated whitespace.
    """

    return (
        series
        .str.replace(
            _WHITESPACE_REGEX,
            " ",
            regex=True,
        )
        .str.strip()
    )


# ============================================================
# PIPELINE STAGES
# ============================================================

def normalize_whitespace(
    series: pd.Series,
) -> pd.Series:
    """
    Initial whitespace cleanup.
    """

    series = _to_string_dtype(series)

    return _collapse_whitespace(series)


def normalize_building_codes(
    series: pd.Series,
) -> pd.Series:
    """
    Canonical building code normalization.
    """

    series = _to_string_dtype(series)

    return (
        series
        .str.upper()
        .str.replace(
            _BUILDING_REGEX,
            "PCC",
            regex=True,
        )
    )


def strip_room_noise(
    series: pd.Series,
) -> pd.Series:
    """
    Removes non-essential room wording.
    """

    series = _to_string_dtype(series)

    series = series.str.replace(
        _ROOM_REGEX,
        "",
        regex=True,
    )

    return _collapse_whitespace(series)


def remove_hyphens(
    series: pd.Series,
) -> pd.Series:
    """
    Removes location hyphen separators.
    """

    series = _to_string_dtype(series)

    return series.str.replace(
        "-",
        "",
        regex=False,
    )


def normalize_off_campus(
    series: pd.Series,
) -> pd.Series:
    """
    Converts all off-campus variants into
    canonical schema value.
    """

    series = _to_string_dtype(series)

    mask = series.str.contains(
        r"(?i)\boff\s*campus\b",
        na=False,
    )

    result = series.copy()

    result.loc[mask] = OFF_CAMPUS_CANONICAL

    return result


def enforce_spacing(
    series: pd.Series,
) -> pd.Series:
    """
    Enforces canonical building-room spacing.
    """

    series = _to_string_dtype(series)

    return series.str.replace(
        _SPACING_REGEX,
        r"\1  \2",
        regex=True,
    )


# ============================================================
# DAG PIPELINE REGISTRY
# ============================================================

_LOCATION_PIPELINE = [
    normalize_whitespace,
    normalize_building_codes,
    strip_room_noise,
    remove_hyphens,
    normalize_off_campus,
    enforce_spacing,
]


# ============================================================
# PUBLIC API
# ============================================================

def normalize_location(
    series: pd.Series,
) -> pd.Series:
    """
    Full deterministic location normalization pipeline.

    IMPORTANT:
    Pipeline order is intentional and stable.
    """

    na_mask = series.isna()

    result = series.copy()

    for transform in _LOCATION_PIPELINE:
        result = transform(result)

    result.loc[na_mask] = pd.NA

    return result