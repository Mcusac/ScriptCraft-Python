"""
Data processing patterns and orchestration utilities.

This module composes higher-level workflows using level_2 as the
SINGLE SOURCE OF TRUTH for processing logic.
"""

import pandas as pd

from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_0.file_ops import (
    find_latest_file,
    find_matching_file,
)
from layers.layer_1_tools.level_0_infra.level_1.paths import FILE_PATTERNS
from layers.layer_1_tools.level_0_infra.level_1.tool_dispatcher import dispatch_tool


# ─────────────────────────────────────────────────────────────
# File setup utilities
# ─────────────────────────────────────────────────────────────

def setup_tool_files(
    paths: Dict[str, Any],
    domain: str,
    tool_name: str
) -> tuple[Optional[Path], Optional[Path]]:

    dataset_file = find_latest_file(paths["merged"])

    dictionary_file = find_matching_file(
        paths["dictionary"],
        FILE_PATTERNS["cleaned_dict"]
    )

    if not dictionary_file:
        dictionary_file = find_matching_file(
            paths["dictionary"],
            FILE_PATTERNS["release_dict"]
        )
        if dictionary_file:
            log_and_print("🟡 Using fallback release dictionary (cleaned version not found).")

    log_and_print(f"\n🚀 Starting {tool_name} for **{domain}**")

    if not dataset_file:
        log_and_print("⚠️ No dataset file found.")
        return None, None

    if not dictionary_file:
        log_and_print("⚠️ No dictionary file found.")
        return None, None

    log_and_print(f"📂 Dataset in use: {dataset_file}")
    log_and_print(f"📂 Dictionary in use: {dictionary_file}")

    return dataset_file, dictionary_file


# ─────────────────────────────────────────────────────────────
# TOOL EXECUTION (NOW DELEGATED)
# ─────────────────────────────────────────────────────────────

def standardize_tool_execution(
    tool_class: type,
    domain: str,
    input_path: str,
    output_path: str,
    paths: Dict[str, Any],
    **kwargs: Any
) -> None:
    """
    Thin wrapper over canonical dispatcher.
    """

    tool = tool_class()

    dispatch_tool(
        tool=tool,
        domain=domain,
        input_path=input_path,
        output_path=output_path,
        paths=paths,
        **kwargs,
    )


def create_tool_runner(
    tool_class: type,
    **default_kwargs: Any
) -> Callable[[str, str, str, Dict[str, Any]], None]:

    def runner(
        domain: str,
        input_path: str,
        output_path: str,
        paths: Dict[str, Any],
        **kwargs: Any
    ) -> None:

        execution_kwargs = {**default_kwargs, **kwargs}

        standardize_tool_execution(
            tool_class,
            domain,
            input_path,
            output_path,
            paths,
            **execution_kwargs,
        )

    return runner


# ─────────────────────────────────────────────────────────────
# DATA UTILITIES (UNCHANGED)
# ─────────────────────────────────────────────────────────────

def merge_dataframes(
    dataframes: List[pd.DataFrame],
    merge_strategy: str = "concat",
    **kwargs: Any
) -> pd.DataFrame:

    if not dataframes:
        return pd.DataFrame()

    if merge_strategy == "concat":
        return pd.concat(dataframes, ignore_index=True, **kwargs)

    if merge_strategy == "merge":
        result = dataframes[0]
        for df in dataframes[1:]:
            result = result.merge(df, **kwargs)
        return result

    raise ValueError(f"Unknown merge strategy: {merge_strategy}")


def merge_with_key_column(
    base_df: pd.DataFrame,
    supplement_df: pd.DataFrame,
    key_column: str,
    update_existing: bool = False,
    log_changes: bool = True
) -> pd.DataFrame:

    merged_df = base_df.copy()
    added_items = []
    updated_items = []

    for _, row in supplement_df.iterrows():
        key_value = str(row.get(key_column)).strip()

        if not key_value:
            continue

        if key_value in merged_df[key_column].values:
            if update_existing:
                idx = merged_df.index[
                    merged_df[key_column] == key_value
                ].tolist()[0]

                for col, val in row.items():
                    if pd.notna(val) and col in merged_df.columns:
                        merged_df.at[idx, col] = val

                updated_items.append(key_value)

        else:
            merged_df = pd.concat(
                [merged_df, row.to_frame().T],
                ignore_index=True
            )
            added_items.append(key_value)

    if log_changes:
        log_and_print(f"➕ Added {len(added_items)} new items")
        if update_existing:
            log_and_print(f"🔄 Updated {len(updated_items)} existing items")

    return merged_df


def process_by_domains(
    data: pd.DataFrame,
    domain_configs: Dict[str, Dict[str, Any]],
    process_func: Callable[[pd.DataFrame, Dict[str, Any]], pd.DataFrame],
    **kwargs: Any
) -> Dict[str, pd.DataFrame]:

    results = {}

    for domain, config in domain_configs.items():
        try:
            log_and_print(f"🔍 Processing domain: {domain}")
            results[domain] = process_func(data, config, **kwargs)
            log_and_print(f"✅ Completed domain: {domain}")

        except Exception as e:
            log_and_print(f"❌ Error processing domain {domain}: {e}", level="error")

    return results


def split_dataframe_by_column(
    df: pd.DataFrame,
    split_column: str,
    reference_data: Dict[str, pd.DataFrame],
    output_dir: Optional[Path] = None
) -> Dict[str, pd.DataFrame]:

    df[split_column] = df[split_column].astype(str).str.strip()

    results = {}
    leftovers = df.copy()

    for split_value, reference_df in reference_data.items():
        reference_values = set(
            reference_df[split_column].dropna().astype(str).str.strip()
        )

        matched = leftovers[leftovers[split_column].isin(reference_values)]
        leftovers = leftovers[~leftovers[split_column].isin(reference_values)]

        if not matched.empty:
            results[split_value] = matched

            if output_dir:
                output_path = output_dir / f"{split_value}_split.xlsx"
                matched.to_excel(output_path, index=False)
                log_and_print(f"💾 Saved {split_value} split: {output_path}")

    if not leftovers.empty and output_dir:
        leftovers_path = output_dir / "leftovers.xlsx"
        leftovers.to_excel(leftovers_path, index=False)
        log_and_print(f"📁 Saved leftovers: {leftovers_path}")

    return results