"""Detect scalar values that should be treated as missing."""

import math
import pandas as pd

from typing import Any

from scriptcraft.layers.layer_0_core.level_0 import (
    MISSING_VALUE_CODES,
    MISSING_VALUE_LITERALS,
    MISSING_VALUE_STRINGS,
)


def is_missing_like(val: Any) -> bool:
    """Return True when a value should be treated as missing."""
    if val is None:
        return True
    try:
        if pd.isna(val):
            return True
    except (TypeError, ValueError):
        pass

    if isinstance(val, float) and math.isnan(val):
        return True

    if isinstance(val, int) and val in MISSING_VALUE_CODES:
        return True

    text = str(val).strip()
    if not text:
        return True
    if text in MISSING_VALUE_LITERALS:
        return True
    if text.lower() in MISSING_VALUE_LITERALS:
        return True
    return text.upper() in MISSING_VALUE_STRINGS
