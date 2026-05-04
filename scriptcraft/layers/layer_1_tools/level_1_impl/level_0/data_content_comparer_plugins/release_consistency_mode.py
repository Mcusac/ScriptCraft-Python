"""
Pipeline orchestration layer.
"""

import pandas as pd

from pathlib import Path

from layers.layer_1_tools.level_0_infra.level_0.release_consistency_mode.comparison_engine import build_pivot, diff_block, diff_filtered
from layers.layer_1_tools.level_0_infra.level_1.release_consistency_mode.dataset_preparation import prepare_dataset
from layers.layer_1_tools.level_0_infra.level_1.release_consistency_mode.dtype_alignment import align_dtypes
from layers.layer_1_tools.level_0_infra.level_1.release_consistency_mode.reporting import write_csv, column_changes


def run_comparison(
    df_old: pd.DataFrame,
    df_new: pd.DataFrame,
    dataset: str,
    output: Path,
    mode: str,
    old_label: str,
    new_label: str,
    config=None,
    debug=False,
):
    df_old, df_new, missing = prepare_dataset(df_old, df_new, config, dataset)

    if debug:
        df_old, df_new = align_dtypes(df_old, df_new, dataset, missing)

    pivot = build_pivot(df_old, df_new, old_label, new_label, drop_release=False)

    strategy = diff_filtered if mode == "filtered" else diff_block
    result = strategy(pivot, old_label, new_label)

    write_csv(result, output, dataset, f"{len(result)} rows written")

    column_changes(set(df_old.columns) - set(df_new.columns),
                   set(df_new.columns) - set(df_old.columns),
                   dataset)