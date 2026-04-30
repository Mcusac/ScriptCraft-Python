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