"""Generic pandas merge helpers (no domain column contracts)."""

import pandas as pd


def outer_merge_with_indicator(
    left: pd.DataFrame,
    right: pd.DataFrame,
    *,
    left_on: str,
    right_on: str,
    indicator_col: str = "merge_flag",
) -> pd.DataFrame:
    """Outer merge with pandas indicator, renaming ``_merge`` to ``indicator_col``."""
    merged = pd.merge(
        left,
        right,
        left_on=left_on,
        right_on=right_on,
        how="outer",
        indicator=True,
        validate="many_to_many",
    )
    return merged.rename(columns={"_merge": indicator_col})
