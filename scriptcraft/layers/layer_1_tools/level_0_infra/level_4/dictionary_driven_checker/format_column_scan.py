"""Column-wise scan for date format compliance."""

import pandas as pd

from typing import List

from scriptcraft.layers.layer_0_core.level_0 import (
    coerce_datetime_with_format,
    FlaggedValue,
)
from scriptcraft.layers.layer_0_core.level_1 import flag_indices
from scriptcraft.layers.layer_0_core.level_2 import filter_non_missing_string_series

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import get_status_emoji
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    empty_scan_result,
    ensure_column_present,
)


def scan_date_format_column(
    df: pd.DataFrame,
    col: str,
    expected_format: str,
) -> List[FlaggedValue]:
    """Flag all rows whose values do not match ``expected_format``."""
    if not ensure_column_present(df, col):
        return empty_scan_result()

    log_and_print(
        f"{get_status_emoji('processing')} Validating dates in '{col}'..."
    )

    series = filter_non_missing_string_series(df[col].astype(str))
    if series.empty:
        log_and_print(
            f"{get_status_emoji('empty')} No date values to validate in '{col}'"
        )
        return empty_scan_result()

    log_and_print(
        f"{get_status_emoji('analyzing')} Checking date format compliance in '{col}'..."
    )

    parsed = coerce_datetime_with_format(series, expected_format)
    invalid_mask = pd.isna(parsed)
    if not invalid_mask.any():
        log_and_print(
            f"{get_status_emoji('valid')} All dates in '{col}' match expected format"
        )
        return empty_scan_result()

    message = (
        f"{get_status_emoji('invalid')} Invalid date format "
        f"(expected: {expected_format})"
    )
    flagged = flag_indices(df, col, series.index[invalid_mask], message, raw_series=series)
    log_and_print(
        f"{get_status_emoji('found_issues')} Found {len(flagged)} date format "
        f"mismatches in '{col}'"
    )
    return flagged
