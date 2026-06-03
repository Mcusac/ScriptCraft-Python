"""Date-format validator plugin registration."""

import pandas as pd

from typing import Any, List, Optional, Set, Tuple

from scriptcraft.layers.layer_0_core.level_0 import FlaggedValue

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import register_validator
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import ColumnValidator
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import date_format_error_message
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    scan_date_format_column,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import get_plugin_config


@register_validator("date")
class DateValidator(ColumnValidator):
    """Validates date values against a configured strftime format."""

    def __init__(self, expected_format: Optional[str] = None) -> None:
        super().__init__()
        date_config = get_plugin_config("date_validation")
        self.expected_format = expected_format or date_config.get(
            "expected_format", "%m/%Y"
        )

    def validate_value(self, value: Any, expected_values: str) -> Optional[str]:
        """Return an error message when a single value fails format compliance."""
        _ = expected_values
        return date_format_error_message(value, self.expected_format)

    def validate_column(
        self,
        df: pd.DataFrame,
        col: str,
        _: Optional[Set[Tuple[float, float]]] = None,
    ) -> List[FlaggedValue]:
        """Column-wise scan: flag all rows with invalid date format."""
        return scan_date_format_column(df, col, self.expected_format)
