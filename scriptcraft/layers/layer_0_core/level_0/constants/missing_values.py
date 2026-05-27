"""Canonical missing-value literals for scalar normalization."""

from typing import FrozenSet

MISSING_VALUE_STRINGS: FrozenSet[str] = frozenset({
    "-9999", "-9999.0",
    "-8888", "-8888.0",
    "-777777", "-777777.0",
    "NAN", "NAT", "NONE", "", "MISSING",
})
