"""Comparison result model for DataFrame diff workflows."""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Set, Tuple

import pandas as pd


@dataclass
class ComparisonResult:
    """High-level comparison result across multiple dimensions."""

    common: Set[str]
    only_in_first: Set[str]
    only_in_second: Set[str]

    differences: Optional[pd.DataFrame] = None
    dtype_mismatches: Optional[Dict[str, Tuple[Any, Any]]] = None
    shape_mismatch: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
    missing_ids: Optional[Tuple[pd.DataFrame, pd.DataFrame]] = None
    index_comparison: Optional[Tuple[Set[Any], Set[Any], Set[Any]]] = None

    def __post_init__(self) -> None:
        if self.dtype_mismatches is None:
            self.dtype_mismatches = {}
