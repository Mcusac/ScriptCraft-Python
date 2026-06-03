"""
Domain-agnostic constants for level_0 consumers.

This module holds enums and literal constants that do not belong to any
single infrastructure concern (paths, logging, environment, etc.).

Pure constants for the system.

NO I/O, NO environment detection, NO config loading.

Safe to import anywhere.
"""

from enum import Enum
from typing import Dict, List


class OutlierMethod(Enum):
    """Statistical method used for outlier detection."""
    IQR = "IQR"
    STD = "STD"

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

DEFAULT_ENCODING: str = "utf-8"
FALLBACK_ENCODING: str = "ISO-8859-1"