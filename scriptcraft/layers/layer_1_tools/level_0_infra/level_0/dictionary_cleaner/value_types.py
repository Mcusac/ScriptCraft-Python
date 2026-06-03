"""Value-type vocabulary used to normalize dictionary `Value Type` cells."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.expected_values import (
    DEFAULT_VALUE_TYPE,
    VALUE_TYPE_MAP,
)


def normalize_value_type(value: str) -> str:
    """Map an arbitrary value-type label to the canonical vocabulary."""
    if not isinstance(value, str):
        return DEFAULT_VALUE_TYPE
    return VALUE_TYPE_MAP.get(value.strip().lower(), DEFAULT_VALUE_TYPE)
