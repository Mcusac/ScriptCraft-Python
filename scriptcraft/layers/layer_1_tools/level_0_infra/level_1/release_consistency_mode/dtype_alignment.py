"""
Dtype alignment logic.

No I/O. No file system. Pure dataframe transforms.
"""

import numpy as np
import pandas as pd

from typing import Dict, List, Tuple, Any

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print


def detect_mismatches(df_old: pd.DataFrame, df_new: pd.DataFrame) -> Dict[str, Tuple[Any, Any]]:
    common = set(df_old.columns) & set(df_new.columns)

    return {
        c: (df_old[c].dtype, df_new[c].dtype)
        for c in common
        if df_old[c].dtype != df_new[c].dtype
    }


def apply_alignment(df_old: pd.DataFrame, mismatches: Dict[str, Tuple[Any, Any]], missing_values: List[str]) -> pd.DataFrame:
    df_old = df_old.copy()

    for col, (_, target_dtype) in mismatches.items():
        try:
            df_old[col] = df_old[col].replace(missing_values, np.nan)
            df_old[col] = df_old[col].astype(target_dtype)
        except Exception as e:
            log_and_print(f"⚠️ dtype fix failed {col}: {e}")

    return df_old


def align_dtypes(df_old, df_new, dataset_name: str, missing_values: List[str]):
    mismatches = detect_mismatches(df_old, df_new)

    if not mismatches:
        log_and_print(f"✅ No dtype mismatches in {dataset_name}")
        return df_old, df_new

    log_and_print(f"🔧 Aligning dtypes in {dataset_name}")

    for c, (a, b) in mismatches.items():
        log_and_print(f" - {c}: {a} → {b}")

    return apply_alignment(df_old, mismatches, missing_values), df_new