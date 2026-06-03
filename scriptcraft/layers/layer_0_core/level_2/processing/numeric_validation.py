"""Dictionary numeric range validation (orchestrates parse + missing + membership)."""

from typing import Any, Optional

from scriptcraft.layers.layer_0_core.level_0 import parse_numeric_ranges, value_in_ranges
from scriptcraft.layers.layer_0_core.level_1 import is_missing_like


def validate_numeric_against_ranges(
    value: Any,
    expected_values: str,
) -> Optional[str]:
    """Return an error message when ``value`` is outside parsed dictionary ranges."""
    if is_missing_like(value):
        return None

    ranges = parse_numeric_ranges(expected_values)
    if not ranges:
        return None

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return "Non-numeric value"

    if value_in_ranges(numeric_value, ranges):
        return None
    return "Outside defined range"
