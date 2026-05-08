# location_transforms.py

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.location_constants import (
    BUILDING_REGEX,
    ROOM_REGEX,
    SPACING_REGEX,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.constants import (
    OFF_CAMPUS_CANONICAL,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.location_primitives import (
    to_string_dtype,
    collapse_whitespace,
)


def normalize_whitespace(series: pd.Series) -> pd.Series:
    series = to_string_dtype(series)
    return collapse_whitespace(series)


def normalize_building_codes(series: pd.Series) -> pd.Series:
    series = to_string_dtype(series)

    return (
        series
        .str.upper()
        .str.replace(BUILDING_REGEX, "PCC", regex=True)
    )


def strip_room_noise(series: pd.Series) -> pd.Series:
    series = to_string_dtype(series)

    series = series.str.replace(ROOM_REGEX, "", regex=True)

    return collapse_whitespace(series)


def remove_hyphens(series: pd.Series) -> pd.Series:
    series = to_string_dtype(series)

    return series.str.replace("-", "", regex=False)


def normalize_off_campus(series: pd.Series) -> pd.Series:
    series = to_string_dtype(series)

    mask = series.str.contains(r"(?i)\boff\s*campus\b", na=False)

    result = series.copy()
    result.loc[mask] = OFF_CAMPUS_CANONICAL

    return result


def enforce_spacing(series: pd.Series) -> pd.Series:
    series = to_string_dtype(series)

    return series.str.replace(SPACING_REGEX, r"\1  \2", regex=True)