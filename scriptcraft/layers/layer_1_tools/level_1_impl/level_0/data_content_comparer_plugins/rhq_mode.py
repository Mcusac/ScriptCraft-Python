import pandas as pd

from pathlib import Path
from typing import Dict, Any, List

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_comparison_datasets
from layers.layer_1_tools.level_0_infra.level_1.dataframe import get_column_letter
from layers.layer_1_tools.level_0_infra.level_2.value_cleaning import normalize_value


def run_mode(input_paths, output_dir, domain=None, **kwargs) -> Dict[str, Any]:
    """RHQ-specific comparison using Med_ID and AgePeriod keys."""

    if not input_paths or len(input_paths) != 2:
        raise ValueError("RHQ mode requires exactly two input files.")

    suffix = f" for domain: {domain}" if domain else ""
    log_and_print(f"📌 Running RHQ Comparison{suffix}...")

    required_keys = [
        "Med_ID",
        "AgePeriod (this is the decade of life starting at 0)",
    ]

    try:
        df1, df2, dataset_name = load_comparison_datasets(input_paths)

        # ----------------------------
        # Validate required keys
        # ----------------------------
        missing_keys = [
            k for k in required_keys if k not in df1.columns or k not in df2.columns
        ]
        if missing_keys:
            raise ValueError(f"Missing required columns: {missing_keys}")

        # ----------------------------
        # Merge datasets on keys
        # ----------------------------
        merged = pd.merge(
            df1,
            df2,
            on=required_keys,
            how="outer",
            suffixes=("_A1", "_A2"),
            indicator=True,
        )

        discrepancies: List[Dict[str, Any]] = []

        column_positions = {col: idx + 1 for idx, col in enumerate(df1.columns)}

        # ----------------------------
        # Core comparison loop
        # ----------------------------
        for idx, row in merged.iterrows():
            for col in df1.columns:
                if col in required_keys:
                    continue

                val1 = row.get(f"{col}_A1", pd.NA)
                val2 = row.get(f"{col}_A2", pd.NA)

                norm_val1 = normalize_value(val1)
                norm_val2 = normalize_value(val2)

                if norm_val1 != norm_val2:
                    col_letter = get_column_letter(column_positions[col])
                    cell_reference = f"{col_letter}{idx + 2}"

                    discrepancies.append(
                        {
                            "Med_ID": row.get("Med_ID"),
                            "AgePeriod": row.get(
                                "AgePeriod (this is the decade of life starting at 0)"
                            ),
                            "Column": col,
                            "Cell": cell_reference,
                            "Assistant1": norm_val1,
                            "Assistant2": norm_val2,
                        }
                    )

        discrepancies_df = pd.DataFrame(discrepancies)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        discrepancy_file = output_dir / f"{dataset_name}_discrepancy_list.xlsx"
        discrepancies_df.to_excel(discrepancy_file, index=False)

        log_and_print(f"📄 Discrepancy report saved to: {discrepancy_file.resolve()}")

        # ----------------------------
        # Upload-ready output
        # ----------------------------
        final_df = df1.copy()
        upload_ready_file = output_dir / f"{dataset_name}_upload_ready.xlsx"
        final_df.to_excel(upload_ready_file, index=False)

        log_and_print(f"📄 Upload-ready file saved to: {upload_ready_file.resolve()}")

        return {
            "mode": "rhq",
            "dataset": dataset_name,
            "outputs": [discrepancy_file, upload_ready_file],
            "discrepancies": len(discrepancies),
            "status": "success",
        }

    except Exception as e:
        log_and_print(f"❌ RHQ comparison failed: {e}")

        return {
            "mode": "rhq",
            "dataset": None,
            "outputs": [],
            "status": "failed",
            "error": str(e),
        }