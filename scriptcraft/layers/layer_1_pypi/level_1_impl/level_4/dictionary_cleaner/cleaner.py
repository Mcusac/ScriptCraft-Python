
from pathlib import Path
from typing import Optional

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print, log_fix_summary
from layers.layer_1_pypi.level_0_infra.level_1.data_loading import load_data

from layers.layer_1_pypi.level_1_impl.level_0.dictionary_cleaner.fix_counts import FixCounter
from layers.layer_1_pypi.level_1_impl.level_3.dictionary_cleaner.value_parser import parse_missing_or_unit, parse_values


def clean_data(file_path: Path, output_folder: Path, *, counter: Optional[FixCounter] = None) -> FixCounter:
    counter = counter or FixCounter.fresh()

    df = load_data(file_path)
    is_imaging = "Missing" in df.columns and "Unit of Measurement" in df.columns
    filename = file_path.name

    if "Value" in df.columns:
        log_and_print("\n--- Unique Values in 'Value' Column (Before Cleaning) ---")
        log_and_print(df["Value"].dropna().unique())

        df["Value"] = df["Value"].apply(lambda x: parse_values(x, filename=filename, counter=counter))

        log_and_print("\n--- Unique Values in 'Value' Column (After Cleaning) ---")
        log_and_print(df["Value"].dropna().unique())
    else:
        log_and_print("⚠️ No 'Value' column found — skipping value cleaning.")

    columns_to_check = ["Missing", "Unit of Measurement"] if is_imaging else ["Missing/Unit of Measure"]
    for col in columns_to_check:
        if col in df.columns:
            log_and_print(f"\n--- Unique Values in '{col}' Column (Before Cleaning) ---")
            log_and_print(df[col].dropna().unique())

            df[col] = df[col].apply(parse_missing_or_unit)

            log_and_print(f"\n--- Unique Values in '{col}' Column (After Cleaning) ---")
            log_and_print(df[col].dropna().unique())

    cleaned_filename = file_path.name if file_path.stem.endswith("_cleaned") else f"{file_path.stem}_cleaned{file_path.suffix}"
    cleaned_path = output_folder / cleaned_filename

    if file_path.suffix == ".csv":
        df.to_csv(cleaned_path, index=False)
    else:
        df.to_excel(cleaned_path, index=False)

    log_and_print(f"\nCleaned file saved as: {cleaned_path}\n")
    log_fix_summary(counter.counts, label=f"Fix Summary for {file_path.name}")

    return counter

