"""Inclusive numeric range membership checks."""

from typing import Set, Tuple


def value_in_ranges(numeric_value: float, ranges: Set[Tuple[float, float]]) -> bool:
    """Return True when ``numeric_value`` falls within any inclusive range."""
    return any(low <= numeric_value <= high for low, high in ranges)
