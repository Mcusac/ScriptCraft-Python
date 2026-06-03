"""Canonical string form for scalar comparison values."""

from typing import Any

from scriptcraft.layers.layer_0_core.level_1 import is_missing_like


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
