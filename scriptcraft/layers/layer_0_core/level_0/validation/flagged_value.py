"""Validation scan result row (tool-agnostic)."""

import pandas as pd

from dataclasses import dataclass
from typing import Any


@dataclass
class FlaggedValue:
    """Container for flagged validation values."""

    row_index: int
    column: str
    value: Any
    message: str

    @staticmethod
    def from_df_row(
        df: pd.DataFrame,
        idx: int,
        col: str,
        value: Any,
        message: str,
    ) -> "FlaggedValue":
        _ = df
        return FlaggedValue(
            row_index=idx,
            column=col,
            value=value,
            message=message,
        )
