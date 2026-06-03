"""Build flagged values from outlier threshold bounds."""

import pandas as pd

from typing import Dict, List, Tuple

from scriptcraft.layers.layer_0_core.level_0 import FlaggedValue
from scriptcraft.layers.layer_0_core.level_1 import flag_indices

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import OutlierMethod
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import get_status_emoji


def flag_numeric_outliers(
    df_clean: pd.DataFrame,
    col: str,
    col_data: pd.Series,
    thresholds: Dict[str, Tuple[float, float]],
    method: OutlierMethod,
) -> List[FlaggedValue]:
    """Flag rows outside any threshold band; each band labeled in the message."""
    flagged: List[FlaggedValue] = []
    outlier_mask = pd.Series(False, index=col_data.index)
    for label, (low, high) in thresholds.items():
        current_mask = (col_data < low) | (col_data > high)
        new_outliers = current_mask & ~outlier_mask
        if new_outliers.any():
            message = (
                f"{get_status_emoji('found_issues')} {method.value} "
                f"Outlier ({label})"
            )
            flagged.extend(
                flag_indices(
                    df_clean,
                    col,
                    col_data.index[new_outliers],
                    message,
                )
            )
        outlier_mask |= current_mask
    return flagged
