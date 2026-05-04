"""
Dataset preparation layer.
"""
import pandas as pd

from typing import Dict, Optional, Tuple, List

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print


def prepare_dataset(
    df_old: pd.DataFrame,
    df_new: pd.DataFrame,
    config: Optional[Dict],
    dataset_name: str,
) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:

    if config:
        drop_cols = config.get("initial_drop_cols", [])
        missing = config.get("missing_values", ["-9999", "-8888"])

        if drop_cols:
            df_old = df_old.drop(columns=drop_cols, errors="ignore")
            df_new = df_new.drop(columns=drop_cols, errors="ignore")
            log_and_print(f"🧹 Dropped: {drop_cols}")
    else:
        missing = ["-9999", "-8888"]

    return df_old, df_new, missing