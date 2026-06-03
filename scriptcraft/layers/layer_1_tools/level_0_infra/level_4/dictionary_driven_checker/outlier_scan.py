"""Column-wise statistical outlier detection."""

from typing import List

import pandas as pd

from scriptcraft.layers.layer_0_core.level_0 import (
    calculate_outlier_thresholds,
    should_skip_outlier_detection,
    FlaggedValue,
)
from scriptcraft.layers.layer_0_core.level_2 import clean_numeric_column_series

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import OutlierMethod, log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import get_status_emoji
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    empty_scan_result,
    ensure_column_present,
    flag_numeric_outliers,
)


def scan_numeric_outliers(
    df: pd.DataFrame,
    col: str,
    method: OutlierMethod,
) -> List[FlaggedValue]:
    """Detect and flag outliers using IQR or STD thresholds."""
    if not ensure_column_present(df, col):
        return empty_scan_result()

    log_and_print(
        f"{get_status_emoji('processing')} Starting outlier detection in '{col}'..."
    )

    col_data = clean_numeric_column_series(df, col)
    if col_data.empty:
        log_and_print(
            f"{get_status_emoji('empty')} No valid numeric data in '{col}'"
        )
        return empty_scan_result()

    if should_skip_outlier_detection(col_data):
        log_and_print(
            f"{get_status_emoji('skipped')} Skipping outlier detection for '{col}' "
            f"- insufficient variation"
        )
        return empty_scan_result()

    df_clean = df.loc[col_data.index]
    log_and_print(
        f"{get_status_emoji('cleaning')} Removed {len(df) - len(df_clean)} "
        f"missing-like values from '{col}' before {method.value} outlier check"
    )

    thresholds = calculate_outlier_thresholds(col_data, method.value)
    flagged = flag_numeric_outliers(df_clean, col, col_data, thresholds, method)

    if flagged:
        log_and_print(
            f"{get_status_emoji('found_issues')} Found {len(flagged)} outliers in "
            f"'{col}' using {method.value}"
        )
    else:
        log_and_print(
            f"{get_status_emoji('success')} No outliers detected in '{col}'"
        )
    return flagged
