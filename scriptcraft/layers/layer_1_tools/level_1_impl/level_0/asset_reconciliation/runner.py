# ============================================================
# runner.py — I/O boundary + comparison orchestration (impl L0)
# ============================================================

from pathlib import Path

import pandas as pd

from scriptcraft.layers.layer_0_core.level_0 import run_nodes
from scriptcraft.layers.layer_0_core.level_4 import load_csv_raw

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    log_and_print,
    write_outputs,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    assert_merged,
    detect_form_duplicates,
    detect_missing,
    emit_input_debug,
    emit_merge_debug,
    run_sanity_checks,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    MERGED_DETECTORS,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    build_device_merged,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_5 import (
    clean_asset_df,
    normalize_form,
)


def run_asset_form_comparison(
    asset_df: pd.DataFrame,
    form_df: pd.DataFrame,
    *,
    debug: bool = False,
) -> dict[str, pd.DataFrame]:
    """Merge asset/form frames, run detectors, return named result tables."""
    emit_input_debug(asset_df, form_df, enabled=debug)

    merged = build_device_merged(asset_df, form_df)
    assert_merged(merged)
    emit_merge_debug(merged, enabled=debug)

    results = run_nodes(merged, MERGED_DETECTORS)

    missing_from_form, only_in_form = detect_missing(merged)
    results["missing_from_form"] = missing_from_form
    results["only_in_form"] = only_in_form
    results["duplicates_in_form"] = detect_form_duplicates(form_df)

    return results


def run(
    asset_csv: str,
    form_csv: str,
    output_dir: Path,
    *,
    debug: bool = False,
) -> None:
    asset_df_raw = load_csv_raw(asset_csv, dtype=str)
    form_df_raw = load_csv_raw(form_csv, dtype=str)

    asset_df = clean_asset_df(asset_df_raw)
    form_df = normalize_form(form_df_raw)

    if debug:
        run_sanity_checks(asset_df, form_df)

    results = run_asset_form_comparison(
        asset_df,
        form_df,
        debug=debug,
    )

    outputs = {f"{key}.csv": value for key, value in results.items()}

    write_outputs(outputs, output_dir)

    log_and_print("\n✅ Asset Reconciliation Complete")
    log_and_print(f"📁 Output: {output_dir}\n")

    for filename, df in outputs.items():
        log_and_print(f"  📄 {filename:<25} → {len(df):>4} row(s)")
