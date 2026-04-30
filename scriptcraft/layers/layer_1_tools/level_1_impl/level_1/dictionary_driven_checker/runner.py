import pandas as pd

from pathlib import Path
from typing import Dict, List, Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_0.paths import OutlierMethod
from layers.layer_1_tools.level_0_infra.level_1.plugin_registry import plugin_registry

from layers.layer_1_tools.level_1_impl.level_0.dictionary_driven_checker.dictionary_validation import validate_against_dictionary
from layers.layer_1_tools.level_1_impl.level_0.dictionary_driven_checker.models import ValidationResult


def run_dictionary_checker(
    df: pd.DataFrame,
    dict_df: pd.DataFrame,
    domain: str,
    output_path: Path,
    outlier_method: OutlierMethod,
    output_filename: Optional[str] = None,
) -> None:
    """Validate dataset against data dictionary with plugin fallbacks."""
    try:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        results: List[ValidationResult] = []
        column_stats: Dict[str, Dict] = {}
        skipped_columns: List[str] = []

        log_and_print(f"\n🔍 Validating {domain} dataset against dictionary...")

        validators = {
            plugin_type: plugin_class(outlier_method) if plugin_type == "numeric" else plugin_class()
            for plugin_type, plugin_class in plugin_registry.get_all_plugins("validator").get("validator", {}).items()
        }

        processed_cols = set()
        for _, row in dict_df.iterrows():
            col = str(row.get("Main Variable", "")).strip()
            if not col or col in processed_cols:
                continue

            processed_cols.add(col)
            if col not in df.columns:
                skipped_columns.append(col)
                continue

            value_type = str(row.get("Value Type", "")).strip().lower()
            expected_values = str(row.get("Expected Values", "")).strip()

            column_stats[col] = {"type": value_type, "total": len(df[col].dropna()), "flagged": 0}

            for idx, value in df[col].items():
                visit = df.at[idx, "Visit"] if "Visit" in df.columns else 1

                error = validate_against_dictionary(value, expected_values, value_type, col)

                if not error:
                    validator = validators.get(value_type)
                    if validator:
                        error = validator.validate_value(value, expected_values)

                if error:
                    results.append(
                        ValidationResult(
                            row_index=idx,
                            visit_number=visit,
                            column=col,
                            value=value,
                            message=error,
                            is_warning=value_type == "numeric",
                        )
                    )
                    column_stats[col]["flagged"] += 1

        if results:
            results_df = pd.DataFrame(
                [
                    {
                        "Row": r.row_index,
                        "Visit": r.visit_number,
                        "Column": r.column,
                        "Value": r.value,
                        "Message": r.message,
                        "Type": "Warning" if r.is_warning else "Error",
                    }
                    for r in results
                ]
            )
            resolved_output_filename = output_filename or f"{domain}_validation_results.csv"
            results_df.to_csv(output_path / resolved_output_filename, index=False)

            total_errors = sum(1 for r in results if not r.is_warning)
            total_warnings = sum(1 for r in results if r.is_warning)
            log_and_print(f"\n📊 Validation Summary for {domain}:")
            log_and_print(f"   • {total_errors} errors")
            log_and_print(f"   • {total_warnings} warnings")
            log_and_print(f"   • {len(skipped_columns)} columns skipped")

            for col, stats in column_stats.items():
                if stats["flagged"] > 0:
                    log_and_print(
                        f"   • {col}: {stats['flagged']} / {stats['total']} "
                        f"values flagged ({stats['type']})"
                    )
        else:
            log_and_print(f"✅ No validation issues found in {domain}")

    except Exception as e:
        log_and_print(f"❌ Error during validation: {str(e)}")
        raise

