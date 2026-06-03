"""
scripts/common/expected_values.py

📖 Utilities for parsing expected value formats from data dictionaries, 
including handling numeric ranges, text values, categorical sets, and loading 
min/max supplements from external files.
"""
import pandas as pd

from pathlib import Path
from typing import Union, Set, Tuple, List, Dict

from scriptcraft.layers.layer_0_core.level_0 import parse_expected_values_with_messages

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print


# ==== 📚 Configuration & Constants ====

NOTES_COLUMN_NAMES: List[str] = ["notes(numeric, integer only, text-don't want \"\", etc)", 'notes']
DATE_KEYWORDS: List[str] = ['date', 'mm/yyyy', 'month/year']

# ==== 📏 Value Parsing Utilities ====

def log_and_extract_expected_values(
    value_string: str,
    strict: bool = False,
) -> Tuple[str, Union[Set[str], List[Tuple[float, float]], Tuple[Set[str], List[Tuple[float, float]]]]]:
    """
    Parse dictionary expected-value text and emit parse diagnostics via ``log_and_print``.

    Args:
        value_string: The raw value string to parse.
        strict: If True, raise exceptions instead of returning UNKNOWN.

    Returns:
        Tuple containing (value_type, parsed_values).
    """
    value_type, parsed, messages = parse_expected_values_with_messages(
        value_string, strict=strict
    )
    for message in messages:
        log_and_print(message)
    return value_type, parsed

# ==== 📄 Min/Max Supplement Loading ====

def load_minmax_updated(file_paths: List[str]) -> pd.DataFrame:
    """
    Load and merge one or more minmaxUpdated files into a 'fake dictionary' DataFrame.

    Args:
        file_paths: List of file paths to process.

    Returns:
        DataFrame with columns: Main Variable, Value, Source.
    """
    all_dict_rows: List[Dict[str, str]] = []

    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            log_and_print(f"❌ File not found: {file_path}")
            continue

        try:
            df = pd.read_excel(file_path)
            log_and_print(f"📖 Successfully loaded {file_path}")
        except Exception as e:
            log_and_print(f"❌ Failed to load {file_path}: {e}")
            continue

        for idx, row in df.iterrows():
            try:
                variable = str(row.get('variable', '')).strip()
                if not variable or variable.lower() == 'nan':
                    log_and_print(f"⚠️ Skipping row {idx}: Empty or invalid variable name")
                    continue

                min_val = row.get('min', '')
                max_val = row.get('max', '')

                notes = next(
                    (str(row.get(col, "")).lower() for col in NOTES_COLUMN_NAMES if pd.notna(row.get(col))), 
                    ""
                )

                if (pd.isna(min_val) or pd.isna(max_val) or 
                    str(min_val).upper() == "N/A" or str(max_val).upper() == "N/A"):
                    if any(kw in notes for kw in DATE_KEYWORDS):
                        value_spec = "Mm/Yyyy"
                        log_and_print(f"📅 Set {variable} as date type")
                    else:
                        value_spec = "Text"
                        log_and_print(f"📝 Set {variable} as text type")
                else:
                    try:
                        min_val_clean = str(min_val).strip()
                        max_val_clean = str(max_val).strip()

                        min_val = float(min_val_clean)
                        max_val = float(max_val_clean)

                        min_val = int(min_val) if min_val.is_integer() else min_val
                        max_val = int(max_val) if max_val.is_integer() else max_val

                        value_spec = f"{{{min_val}-{max_val}}}"
                        log_and_print(f"📊 Set {variable} range to {min_val}-{max_val}")
                    except Exception as e:
                        log_and_print(f"⚠️ Could not convert {variable} min={min_val} max={max_val}: {e}")
                        value_spec = "Numeric"

                all_dict_rows.append({
                    "Main Variable": variable,
                    "Value": value_spec,
                    "Source": "supplement"
                })

            except Exception as e:
                log_and_print(f"❌ Error processing row {idx}: {e}")
                continue

    result_df = pd.DataFrame(all_dict_rows)
    log_and_print(f"✅ Processed {len(result_df)} valid rows from {len(file_paths)} files")
    return result_df
