# ============================================================
# runner.py — I/O layer (pure boundary)
# ============================================================

import pandas as pd

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import (
    ASSET_RAW,
    FORM_RAW,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_3.asset_normalizer import clean_asset_df
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_3.form_pipeline import normalize_form
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_4.orchestrator import run_comparison


# ------------------------------------------------------------
# MAIN ENTRY
# ------------------------------------------------------------

def run(
    asset_csv: str,
    form_csv: str,
    output_dir: Path,
    *,
    debug: bool = False,
) -> None:

    # --------------------------------------------------------
    # STEP 1 — LOAD RAW DATA (CSV → pandas)
    # --------------------------------------------------------
    asset_df_raw = pd.read_csv(asset_csv)
    form_df_raw = pd.read_csv(form_csv)

    # --------------------------------------------------------
    # STEP 2 — INGESTION LAYER (CRITICAL FIX)
    # CSV columns → canonical schema fields
    # --------------------------------------------------------
    asset_df = clean_asset_df(asset_df_raw)
    form_df = normalize_form(form_df_raw)

    print("\n--- RUNNER DEBUG (POST-NORMALIZATION) ---")
    print(f"Form rows: {len(form_df)}")
    print(f"Asset rows: {len(asset_df)}")

    print("\nForm tag sample:")
    print(form_df[FORM_RAW.tag].head(10).tolist())

    print("\nAsset tag sample:")
    print(asset_df[ASSET_RAW.tag].head(10).tolist())

    print("\nOverlap estimate:")
    asset_set = set(asset_df[ASSET_RAW.tag].dropna().astype(str))
    form_set = set(form_df[FORM_RAW.tag].dropna().astype(str))

    print(len(asset_set.intersection(form_set)))

    # --------------------------------------------------------
    # STEP 3 — PIPELINE EXECUTION (DAG orchestrator)
    # --------------------------------------------------------
    results = run_comparison(
        asset_df,
        form_df,
        debug=debug,
    )

    # --------------------------------------------------------
    # STEP 4 — OUTPUT DIRECTORY
    # --------------------------------------------------------
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # STEP 5 — OUTPUT MAP (contract outputs only)
    # --------------------------------------------------------
    outputs = {
        "missing_from_form.csv": results["missing_from_form"],
        "only_in_form.csv": results["only_in_form"],
        "location_changes.csv": results["location_changes"],
        "custodian_changes.csv": results["custodian_changes"],
        "duplicate_results.csv": results["duplicate_results"],
        "off_campus.csv": results.get("off_campus", pd.DataFrame()),
    }

    # --------------------------------------------------------
    # STEP 6 — WRITE OUTPUTS
    # --------------------------------------------------------
    for filename, df in outputs.items():
        df.to_csv(output_dir / filename, index=False)

    # --------------------------------------------------------
    # STEP 7 — SUMMARY
    # --------------------------------------------------------
    print("\n✅ Asset Reconciliation Complete")
    print(f"📁 Output: {output_dir}\n")

    for filename, df in outputs.items():
        print(f"  📄 {filename:<25} → {len(df):>4} row(s)")