"""Heuristics for skipping low-signal outlier detection."""

import pandas as pd


def should_skip_outlier_detection(col_data: pd.Series) -> bool:
    """Return True when variation is too low for meaningful outlier checks."""
    return (
        col_data.nunique() <= 1
        or col_data.std() < 0.01
        or (
            set(col_data.unique()).issubset({0, 1})
            and col_data.sum() <= 5
        )
        or (col_data.max() <= 10 and col_data.nunique() <= 10)
    )
