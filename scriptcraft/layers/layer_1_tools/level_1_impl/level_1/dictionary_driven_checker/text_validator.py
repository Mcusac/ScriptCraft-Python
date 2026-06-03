"""Text validator plugin registration."""

import pandas as pd

from typing import Any, List, Optional

from scriptcraft.layers.layer_0_core.level_0 import FlaggedValue

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import register_validator
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import ColumnValidator
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    scan_rare_text_values,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import get_plugin_config


@register_validator("text")
class TextValidator(ColumnValidator):
    """Flags rare text values via optional column-wise scans."""

    def __init__(self, rare_threshold: Optional[int] = None) -> None:
        super().__init__()
        text_config = get_plugin_config("text_validation")
        self.rare_threshold = rare_threshold or text_config.get("rare_threshold", 3)

    def validate_value(self, value: Any, expected_values: str) -> Optional[str]:
        """Per-value hook; rare-value detection requires a column scan."""
        _ = (value, expected_values)
        return None

    def validate_column(
        self,
        df: pd.DataFrame,
        col: str,
        _: None = None,
    ) -> List[FlaggedValue]:
        """Column-wise scan: flag values below the rare-value frequency threshold."""
        return scan_rare_text_values(df, col, self.rare_threshold)
