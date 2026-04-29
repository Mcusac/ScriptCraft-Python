
from typing import Any, Dict, Optional

import pandas as pd

from layers.layer_1_pypi.level_0_infra.level_1.comparison import compare_dataframes


def compare_datasets(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    *,
    comparison_type: str = "full",
    domain: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Compare two datasets and return comparison results.

    `comparison_type` is reserved for future behavior (currently uses a single comparer).
    """
    if domain:
        df1 = df1[df1["Domain"] == domain].copy()
        df2 = df2[df2["Domain"] == domain].copy()

    _ = comparison_type  # extension point
    return compare_dataframes(df1, df2)

