# location_primitives.py

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_0.location_constants import STRING_DTYPE, WHITESPACE_REGEX


def to_string_dtype(series: pd.Series) -> pd.Series:
    return series.astype(STRING_DTYPE)


def collapse_whitespace(series: pd.Series) -> pd.Series:
    return (
        series
        .str.replace(WHITESPACE_REGEX, " ", regex=True)
        .str.strip()
    )