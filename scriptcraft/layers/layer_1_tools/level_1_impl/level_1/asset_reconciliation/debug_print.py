# ============================================================
# debug_print.py — debug rendering layer
#
# DESIGN:
# - Rendering ONLY
# - No business logic
# - No dataframe computation logic
# - All analytics delegated to debug_core
# - Fully DAG-safe
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    get_dataframe_summary,
    get_merge_summary,
)


# ============================================================
# INTERNAL RENDER HELPERS
# ============================================================

def _print_header(title: str) -> None:
    print(f"\n--- {title} ---")


def _print_key_value(label: str, value) -> None:
    print(f"{label}: {value}")


def _print_optional_metric(
    label: str,
    value,
) -> None:
    """
    Prints metric only when value exists.
    """

    if value is not None:
        _print_key_value(label, value)


# ============================================================
# RAW INPUT DEBUG
# ============================================================

def debug_raw_inputs(
    asset_df: pd.DataFrame,
    form_df: pd.DataFrame,
    tag_col: str,
) -> None:
    """
    Renders lightweight raw-ingestion diagnostics.
    """

    _print_header("DEBUG: RAW INPUT")

    asset_summary = get_dataframe_summary(
        asset_df,
        tag_col,
    )

    form_summary = get_dataframe_summary(
        form_df,
        tag_col,
    )

    _print_key_value(
        "Asset rows",
        asset_summary["rows"],
    )

    _print_key_value(
        "Form rows",
        form_summary["rows"],
    )

    _print_optional_metric(
        "Unique asset tags",
        asset_summary["unique_keys"],
    )

    _print_optional_metric(
        "Unique form tags",
        form_summary["unique_keys"],
    )


# ============================================================
# MERGE DEBUG
# ============================================================

def debug_merge(
    merged: pd.DataFrame,
    tag_col: str,
    merge_col: str = "_merge",
) -> None:
    """
    Renders merge diagnostics only.
    """

    _print_header("DEBUG: MERGE RESULTS")

    summary = get_merge_summary(
        merged,
        merge_col,
    )

    if "error" in summary:
        print("⚠️ Missing merge column")
        return

    print(summary["distribution"])

    print("\nSample rows:")

    print(
        merged[
            [tag_col, merge_col]
        ].head(10)
    )