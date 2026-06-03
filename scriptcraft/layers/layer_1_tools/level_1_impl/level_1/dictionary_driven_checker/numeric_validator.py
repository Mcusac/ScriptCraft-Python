"""Numeric validator plugin registration."""

import pandas as pd

from typing import Any, List, Optional, Set, Tuple

from scriptcraft.layers.layer_0_core.level_0 import FlaggedValue
from scriptcraft.layers.layer_0_core.level_2 import validate_numeric_against_ranges

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import OutlierMethod
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import register_validator
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import ColumnValidator
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    scan_numeric_ranges,
    scan_numeric_outliers,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import get_dictionary_checker_config


@register_validator("numeric")
class NumericValidator(ColumnValidator):
    """Validates numeric values (ranges per-value; outliers via column scan)."""

    def __init__(self, method: Optional[OutlierMethod] = None) -> None:
        super().__init__(method)
        checker_config = get_dictionary_checker_config()
        configured = checker_config.get("outlier_method", "IQR")
        self.method = method or getattr(OutlierMethod, str(configured), OutlierMethod.IQR)

    def validate_value(self, value: Any, expected_values: str) -> Optional[str]:
        """Per-value range validation using dictionary expected-values text."""
        return validate_numeric_against_ranges(value, expected_values)

    def validate_column(
        self,
        df: pd.DataFrame,
        col: str,
        expected_values: Optional[Set[Tuple[float, float]]] = None,
    ) -> List[FlaggedValue]:
        """Column-wise scan: range checks and/or outlier detection."""
        if expected_values:
            return scan_numeric_ranges(df, col, expected_values)
        return scan_numeric_outliers(df, col, self.method)
