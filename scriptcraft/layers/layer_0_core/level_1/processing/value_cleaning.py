"""Value-level scalar normalization for comparisons."""

import pandas as pd

from typing import Any

from scriptcraft.layers.layer_0_core.level_0 import MISSING_VALUE_STRINGS


def is_missing_like(val: Any) -> bool:
    """Determine whether a value should be treated as missing."""
    if pd.isna(val):
        return True
    return str(val).strip().upper() in MISSING_VALUE_STRINGS


def normalize_value(val: Any) -> str:
    """
    Normalize scalar value:
    - missing -> 'MISSING'
    - numeric -> compact string form
    - string -> stripped
    """
    if is_missing_like(val):
        return "MISSING"

    if isinstance(val, (int, float)):
        return str(int(val)) if float(val).is_integer() else str(val)

    return str(val).strip()
