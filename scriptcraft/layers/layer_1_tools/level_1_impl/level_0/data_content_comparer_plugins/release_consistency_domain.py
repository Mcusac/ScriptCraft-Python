"""Domain logic: compare two release DataFrames and write a diff report."""

from typing import Any

import pandas as pd

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import build_pivot, diff_block, diff_filtered
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    align_dtypes,
    column_changes,
    prepare_dataset,
    write_csv,
)


def compare_release_dataframes(
    df_old: pd.DataFrame,
    df_new: pd.DataFrame,
    dataset: str,
    output: Path,
    mode: str,
    old_label: str,
    new_label: str,
    config: Any = None,
    debug: bool = False,
) -> None:
    """Pivot two release frames, diff them, and write the result CSV."""
    df_old, df_new, missing = prepare_dataset(df_old, df_new, config, dataset)

    if debug:
        df_old, df_new = align_dtypes(df_old, df_new, dataset, missing)

    pivot = build_pivot(df_old, df_new, old_label, new_label, drop_release=False)

    strategy = diff_filtered if mode == "filtered" else diff_block
    result = strategy(pivot, old_label, new_label)

    write_csv(result, output, dataset, f"{len(result)} rows written")

    column_changes(
        set(df_old.columns) - set(df_new.columns),
        set(df_new.columns) - set(df_old.columns),
        dataset,
    )
