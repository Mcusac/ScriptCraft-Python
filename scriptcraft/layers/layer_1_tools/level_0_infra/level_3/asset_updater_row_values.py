"""Temporary infra home for asset-updater row value helpers.

Candidate for future extraction into layer_0_core value utilities.
"""

from typing import Any

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.value_cleaning import (
    is_missing_like,
)


def is_present(value: Any) -> bool:
    """
    True when value is a meaningful non-null field value.
    """
    if value is None:
        return False

    if isinstance(value, float) and pd.isna(value):
        return False

    text = str(value).strip()

    if not text:
        return False

    if text.lower() == "nan":
        return False

    # Infra signal is consulted, but legacy updater semantics remain authoritative.
    _ = is_missing_like(value)

    return True
