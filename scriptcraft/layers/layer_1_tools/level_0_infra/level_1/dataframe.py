"""
Utility functions for working with pandas DataFrames (logging-aware helpers).

For pure diagnostics (stats, dtypes, duplicates), use
``scriptcraft.layers.layer_0_core.level_1.data.tabular_diagnostics``.
"""

import pandas as pd

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print


def display_missing_values(
    data_dict: Dict[str, pd.DataFrame],
    output_file: Optional[Union[str, Path]] = None,
) -> None:
    """Display missing value counts for each dataset and optionally save to file."""
    output = []
    for name, df in data_dict.items():
        missing_counts = df.isna().sum().sort_values(ascending=False)
        missing_counts = missing_counts[missing_counts > 0]
        if not missing_counts.empty:
            info = f"\n🔍 Missing Values in {name}:\n{missing_counts.to_string()}"
            log_and_print(info)
            output.append(info)

    if output_file and output:
        with open(output_file, "a", encoding="utf-8") as f:
            f.writelines(output)


def normalize_column_names(
    df: pd.DataFrame,
    alias_map: Dict[str, List[str]],
    required_columns: Optional[List[str]] = None,
    context_label: str = "",
) -> pd.DataFrame:
    """Standardize DataFrame column names based on a provided alias map."""
    rename_map = {}
    for standard_name, aliases in alias_map.items():
        for alias in aliases:
            if alias in df.columns:
                rename_map[alias] = standard_name

    if rename_map:
        log_and_print(f"🔧 [{context_label}] Renamed columns: {rename_map}")
    else:
        log_and_print(f"ℹ️ [{context_label}] No column renaming needed.")

    df = df.rename(columns=rename_map)

    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            log_and_print(
                f"⚠️ [{context_label}] Missing expected standardized columns after renaming: {missing}"
            )

    return df


def apply_safe_transform(
    df: pd.DataFrame,
    columns: List[str],
    transform_fn: Callable[[Any], Any],
    error_value: Optional[Any] = None,
) -> pd.DataFrame:
    """Safely applies a transformation function to specified columns."""
    result = df.copy()
    for col in columns:
        if col in df.columns:
            try:
                result[col] = df[col].apply(
                    lambda x: transform_fn(x) if pd.notna(x) else x
                )
            except Exception as e:
                log_and_print(f"⚠️ Error transforming column {col}: {str(e)}")
                if error_value is not None:
                    result[col] = error_value
    return result
