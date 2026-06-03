"""Column-wise scan for numeric values outside defined ranges."""

import pandas as pd

from typing import List, Set, Tuple

from scriptcraft.layers.layer_0_core.level_0 import FlaggedValue
from scriptcraft.layers.layer_0_core.level_1 import flag_indices

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import get_status_emoji
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    empty_scan_result,
    ensure_column_present,
)


def scan_numeric_ranges(
    df: pd.DataFrame,
    col: str,
    ranges: Set[Tuple[float, float]],
) -> List[FlaggedValue]:
    """Flag values that fall outside any of the given inclusive ranges."""
    if not ensure_column_present(df, col):
        return empty_scan_result()

    series = df[col].dropna()
    log_and_print(
        f"{get_status_emoji('processing')} Validating ranges in '{col}'..."
    )

    numeric_series = pd.to_numeric(series, errors="coerce")
    in_range_mask = pd.Series(False, index=series.index)
    for low, high in ranges:
        in_range_mask |= (numeric_series >= low) & (numeric_series <= high)

    outside_range_idx = series.index[~in_range_mask]
    flagged: List[FlaggedValue] = []
    for idx in outside_range_idx:
        if pd.isna(numeric_series[idx]):
            message = f"{get_status_emoji('invalid')} Non-numeric in range column"
        else:
            message = f"{get_status_emoji('invalid')} Outside defined range"
        flagged.extend(flag_indices(df, col, [idx], message, raw_series=series))

    if flagged:
        log_and_print(
            f"{get_status_emoji('found_issues')} Found {len(flagged)} values outside "
            f"defined ranges in '{col}'"
        )
    else:
        log_and_print(
            f"{get_status_emoji('valid')} All values in '{col}' are within defined ranges"
        )
    return flagged
