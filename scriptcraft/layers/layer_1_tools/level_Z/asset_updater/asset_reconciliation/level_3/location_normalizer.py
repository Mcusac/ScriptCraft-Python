# location_pipeline.py

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.location_constants import DEBUG_LOCATION_PIPELINE
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_2.location_transforms import (
    normalize_whitespace,
    normalize_building_codes,
    strip_room_noise,
    remove_hyphens,
    normalize_off_campus,
    enforce_spacing,
)


_LOCATION_PIPELINE = [
    normalize_whitespace,
    normalize_building_codes,
    strip_room_noise,
    remove_hyphens,
    normalize_off_campus,
    enforce_spacing,
]


def _debug(stage: str, series: pd.Series):
    if DEBUG_LOCATION_PIPELINE:
        print(f"\n--- {stage} ---")
        print(series.head(10))


def normalize_location(series: pd.Series) -> pd.Series:
    na_mask = series.isna()
    result = series.copy()

    _debug("INPUT", result)

    for transform in _LOCATION_PIPELINE:
        before = result.copy()

        result = transform(result)

        _debug(transform.__name__, result)

        if DEBUG_LOCATION_PIPELINE:
            print(f"Changed count: {(before != result).sum()}")

    result.loc[na_mask] = pd.NA

    _debug("FINAL", result)

    return result