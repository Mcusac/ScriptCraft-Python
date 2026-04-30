import pandas as pd

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_comparison_datasets
from layers.layer_1_tools.level_0_infra.level_1.cleaning import normalize_value
from layers.layer_1_tools.level_0_infra.level_1.dataframe import get_column_letter



def run_mode(input_paths, output_dir, domain=None, **kwargs) -> None:
    """RHQ-specific comparison using Med_ID and AgePeriod keys."""
    if not input_paths:
        raise ValueError("RHQ mode requires two input files provided via --input.")

    log_and_print(f"📌 Running RHQ Comparison{' for domain: ' + domain if domain else ''}...")

    required_keys = ["Med_ID", "AgePeriod (this is the decade of life starting at 0)"]

    df1, df2, dataset_name = load_comparison_datasets(input_paths)

    for key in required_keys:
        if key not in df1.columns or key not in df2.columns:
            raise ValueError(f"Missing required column '{key}' in one or both datasets.")

    merged = pd.merge(
        df1,
        df2,
        on=required_keys,
        how="outer",
        suffixes=("_Assistant1", "_Assistant2"),
        indicator=True,
    )

    discrepancies = []

    column_positions = {col: idx + 1 for idx, col in enumerate(df1.columns)}

    for idx, row in merged.iterrows():
        for col in df1.columns:
            if col in required_keys:
                continue  # Skip merge keys
            val1 = row.get(f"{col}_Assistant1", pd.NA)
            val2 = row.get(f"{col}_Assistant2", pd.NA)
            norm_val1 = normalize_value(val1)
            norm_val2 = normalize_value(val2)
            if norm_val1 != norm_val2:
                cell_reference = f"{get_column_letter(column_positions[col])}{idx + 2}"
                discrepancies.append(
                    {
                        "Med_ID": row["Med_ID"],
                        "AgePeriod": row["AgePeriod (this is the decade of life starting at 0)"],
                        "Column": col,
                        "Cell": cell_reference,
                        "Assistant1": norm_val1,
                        "Assistant2": norm_val2,
                    }
                )

    discrepancies_df = pd.DataFrame(discrepancies)

    discrepancy_file = output_dir / f"{dataset_name}_discrepancy_list.xlsx"
    discrepancies_df.to_excel(discrepancy_file, index=False)
    log_and_print(f"📄 Discrepancy report saved to: {discrepancy_file.resolve()}")

    # Optional: Generate upload-ready file using Assistant1 values by default
    final_df = df1.copy()
    upload_ready_file = output_dir / f"{dataset_name}_upload_ready.xlsx"
    final_df.to_excel(upload_ready_file, index=False)
    log_and_print(f"📄 Upload-ready file saved to: {upload_ready_file.resolve()}")

