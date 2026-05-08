# ============================================================
# runner.py — PURE I/O BOUNDARY
# ============================================================

from pathlib import Path
import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.loader import (
    load_csv,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.writer import (
    write_outputs,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.sanity_checks import (
    run_sanity_checks,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_6.asset_ingest import (
    ingest_assets,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_6.form_ingest import (
    ingest_forms,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_6.orchestrator import (
    run_comparison,
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
    asset_df_raw = load_csv(asset_csv)
    form_df_raw = load_csv(form_csv)

    # --------------------------------------------------------
    # STEP 2 — INGESTION
    # --------------------------------------------------------
    asset_df = ingest_assets(asset_df_raw)
    form_df = ingest_forms(form_df_raw)

    # --------------------------------------------------------
    # STEP 3 — DEBUG (OPTIONAL)
    # --------------------------------------------------------
    if debug:
        run_sanity_checks(asset_df, form_df)

    # --------------------------------------------------------
    # STEP 4 — PIPELINE EXECUTION
    # --------------------------------------------------------
    results = run_comparison(
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
    print("\n✅ Asset Reconciliation Complete")
    print(f"📁 Output: {output_dir}\n")

    for filename, df in outputs.items():
        print(f"  📄 {filename:<25} → {len(df):>4} row(s)")