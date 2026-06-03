"""Helpers for building column-scan validation results."""

import pandas as pd

from typing import Iterable, List, Union

from scriptcraft.layers.layer_0_core.level_0 import FlaggedValue

IndexLike = Union[pd.Index, Iterable[int]]


def flag_indices(
    df: pd.DataFrame,
    col: str,
    indices: IndexLike,
    message: str,
    *,
    raw_series: pd.Series | None = None,
) -> List[FlaggedValue]:
    """Build ``FlaggedValue`` rows for the given dataframe indices."""
    flagged: List[FlaggedValue] = []
    source = raw_series if raw_series is not None else df[col]
    for idx in indices:
        flagged.append(
            FlaggedValue.from_df_row(
                df,
                idx,
                col,
                source.loc[idx] if idx in source.index else df.loc[idx, col],
                message,
            )
        )
    return flagged
