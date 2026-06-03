"""Series-level filters built on missing-value detection."""

import pandas as pd

from scriptcraft.layers.layer_0_core.level_1 import is_missing_like


def filter_non_missing_string_series(series: pd.Series) -> pd.Series:
    """Drop missing-like entries from a string-cast column series."""
    if series.empty:
        return series
    mask = ~series.map(is_missing_like)
    return series[mask]
