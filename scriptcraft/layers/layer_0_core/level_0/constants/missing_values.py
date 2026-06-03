"""Canonical missing-value literals for scalar normalization."""

from typing import FrozenSet

MISSING_VALUE_STRINGS: FrozenSet[str] = frozenset({
    "-9999", "-9999.0",
    "-8888", "-8888.0",
    "-777777", "-777777.0",
    "NAN", "NAT", "NONE", "", "MISSING",
})

MISSING_VALUE_CODES: FrozenSet[int] = frozenset({-9999, -8888, -777777})

# Common string sentinels seen in clinical/export spreadsheets.
MISSING_VALUE_LITERALS: FrozenSet[str] = frozenset({
    "",
    ".",
    "-",
    "--",
    "nan",
    "NaN",
    "NA",
    "N/A",
    "null",
    "None",
    "none",
    "#N/A",
    "#NA",
})
