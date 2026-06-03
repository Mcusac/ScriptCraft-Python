"""Column-wise scan for infrequently occurring text values."""

import pandas as pd

from typing import List

from scriptcraft.layers.layer_0_core.level_0 import FlaggedValue
from scriptcraft.layers.layer_0_core.level_1 import flag_indices
from scriptcraft.layers.layer_0_core.level_2 import filter_non_missing_string_series

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import get_status_emoji
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    empty_scan_result,
    ensure_column_present,
)


def scan_rare_text_values(
    df: pd.DataFrame,
    col: str,
    rare_threshold: int,
) -> List[FlaggedValue]:
    """Flag values that appear fewer than ``rare_threshold`` times in the column."""
    if not ensure_column_present(df, col, log_warnings=False):
        return empty_scan_result()

    series = filter_non_missing_string_series(df[col].astype(str))
    if series.empty:
        return empty_scan_result()

    value_counts = series.value_counts(dropna=False)
    rare_values = value_counts[value_counts < rare_threshold].index
    rare_mask = series.isin(rare_values)
    if not rare_mask.any():
        return empty_scan_result()

    message = f"Rare Value (seen < {rare_threshold} times)"
    flagged = flag_indices(df, col, series.index[rare_mask], message, raw_series=series)
    log_and_print(
        f"{get_status_emoji('found_issues')} Found {len(flagged)} rare values in "
        f"'{col}' (threshold: {rare_threshold})"
    )
    return flagged
