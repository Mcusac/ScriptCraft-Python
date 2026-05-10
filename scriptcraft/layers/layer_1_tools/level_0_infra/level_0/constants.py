"""
Domain-agnostic constants for level_0 consumers.

This module holds enums and literal constants that do not belong to any
single infrastructure concern (paths, logging, environment, etc.).
"""

from enum import Enum


class OutlierMethod(Enum):
    """Statistical method used for outlier detection."""
    IQR = "IQR"
    STD = "STD"

"""
Pure constants for the system.

NO I/O, NO environment detection, NO config loading.
Safe to import anywhere.
"""

from typing import Dict, FrozenSet, List


STANDARD_KEYS: Dict[str, str] = {
    "input": "processed_data",
    "output": "qc_output",
    "dictionary": "dictionary",
    "merged_data": "merged_data",
}

FILE_PATTERNS: Dict[str, str] = {
    "final_csv": r"_FINAL\.(csv|xlsx|xls)$",
    "release_dict": r"_Release\.(csv|xlsx|xls)$",
    "clinical_final": r"Clinical_FINAL\.(csv|xlsx)$",
    "cleaned_dict": r"_cleaned\.(csv|xlsx)$",
    "supplement": r"_supplement\.(csv|xlsx|xls)$",
}

COLUMN_ALIASES: Dict[str, List[str]] = {
    "Med_ID": ["Med ID", "MedID", "Med id", "Med Id"],
    "Visit_ID": ["Visit_ID", "Visit ID", "Visit", "Visit id", "Visit Id"],
}

MISSING_VALUE_CODES: List[int] = [-9999, -8888, -777777]

MISSING_VALUE_STRINGS: FrozenSet[str] = frozenset({
    "-9999", "-9999.0",
    "-8888", "-8888.0",
    "-777777", "-777777.0",
    "NAN", "NAT", "NONE", "", "MISSING",
})

DEFAULT_ENCODING: str = "utf-8"
FALLBACK_ENCODING: str = "ISO-8859-1"