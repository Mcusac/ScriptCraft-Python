"""Column-scan guards with optional tools logging."""

import pandas as pd

from typing import List

from scriptcraft.layers.layer_0_core.level_0 import FlaggedValue

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import get_status_emoji


def ensure_column_present(
    df: pd.DataFrame,
    col: str,
    *,
    log_warnings: bool = True,
) -> bool:
    """Return False when ``col`` is absent (optionally logging a warning)."""
    if col in df.columns:
        return True
    if log_warnings:
        log_and_print(
            f"{get_status_emoji('warning')} Column '{col}' not found in dataframe"
        )
    return False


def empty_scan_result() -> List[FlaggedValue]:
    return []
