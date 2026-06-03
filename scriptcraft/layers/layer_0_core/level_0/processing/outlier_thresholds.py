"""Reusable IQR and STD outlier bound calculators for numeric series."""

from typing import Dict, Tuple

import pandas as pd


def calculate_outlier_thresholds(
    series: pd.Series,
    method: str,
) -> Dict[str, Tuple[float, float]]:
    """Calculate reusable IQR or STD outlier bounds for a numeric series."""
    if method == "STD":
        mean, std = series.mean(), series.std()
        return {
            "3.0*STD": (mean - 3.0 * std, mean + 3.0 * std),
            "2.0*STD": (mean - 2.0 * std, mean + 2.0 * std),
        }

    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    return {
        "3.0*IQR": (q1 - 3.0 * iqr, q3 + 3.0 * iqr),
        "2.0*IQR": (q1 - 2.0 * iqr, q3 + 2.0 * iqr),
        "1.5*IQR": (q1 - 1.5 * iqr, q3 + 1.5 * iqr),
    }
