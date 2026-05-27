# ============================================================
# runner.py — PURE I/O BOUNDARY
# ============================================================

from pathlib import Path

from scriptcraft.layers.layer_0_core.level_4 import load_csv_raw

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    log_and_print,
    write_outputs,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    run_sanity_checks,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_5 import (
    clean_asset_df,
    normalize_form,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    run_asset_form_comparison,
)


def run(
    asset_csv: str,
    form_csv: str,
    output_dir: Path,
    *,
    debug: bool = False,
) -> None:

    # --------------------------------------------------------
    # STEP 1 — LOAD CSV
    # --------------------------------------------------------
    asset_df_raw = load_csv_raw(asset_csv, dtype=str)
    form_df_raw = load_csv_raw(form_csv, dtype=str)

    # --------------------------------------------------------
    # STEP 2 — INGESTION
    # --------------------------------------------------------
    asset_df = clean_asset_df(asset_df_raw)
    form_df = normalize_form(form_df_raw)

    # --------------------------------------------------------
    # STEP 3 — DEBUG (OPTIONAL)
    # --------------------------------------------------------
    if debug:
        run_sanity_checks(asset_df, form_df)

    # --------------------------------------------------------
    # STEP 4 — PIPELINE EXECUTION
    # --------------------------------------------------------
    results = run_asset_form_comparison(
        asset_df,
        form_df,
        debug=debug,
    )

    # --------------------------------------------------------
    # STEP 5 — OUTPUT (NO HARDCODING CONTRACT KEYS)
    # --------------------------------------------------------
    outputs = {
        f"{key}.csv": value
        for key, value in results.items()
    }

    # --------------------------------------------------------
    # STEP 6 — WRITE OUTPUTS
    # --------------------------------------------------------
    write_outputs(outputs, output_dir)

    # --------------------------------------------------------
    # STEP 7 — SUMMARY
    # --------------------------------------------------------
    log_and_print("\n✅ Asset Reconciliation Complete")
    log_and_print(f"📁 Output: {output_dir}\n")

    for filename, df in outputs.items():
        log_and_print(f"  📄 {filename:<25} → {len(df):>4} row(s)")