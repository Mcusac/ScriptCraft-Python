"""
Data processor utilities for common data processing patterns.

This module is the SINGLE SOURCE OF TRUTH for:
- Loading
- Validation
- Processing
- Saving
"""

import pandas as pd

from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Callable, Tuple

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_0.directory_ops import ensure_output_dir
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_data


class DataProcessor:
    """Standardized data processor for common data processing patterns."""

    def __init__(self, name: str = "DataProcessor") -> None:
        self.name = name

    def load_and_validate(
        self,
        input_paths: Union[str, Path, List[Union[str, Path]]],
        required_columns: Optional[List[str]] = None,
        **kwargs: Any
    ) -> Union[pd.DataFrame, List[pd.DataFrame]]:
        if isinstance(input_paths, (str, Path)):
            input_paths = [input_paths]

        dataframes = []

        for path in input_paths:
            try:
                df = load_data(path, **kwargs)

                if df is None:
                    log_and_print(f"⚠️ Failed to load {path}")
                    continue

                if required_columns:
                    missing = set(required_columns) - set(df.columns)
                    if missing:
                        log_and_print(f"⚠️ Missing required columns in {path}: {missing}")

                dataframes.append(df)

                log_and_print(
                    f"✅ Loaded {Path(path).name}: "
                    f"{df.shape[0]} rows, {df.shape[1]} columns"
                )

            except Exception as e:
                log_and_print(f"❌ Error loading {path}: {e}")
                raise

        if not dataframes:
            raise ValueError("No valid dataframes were loaded.")

        return dataframes[0] if len(dataframes) == 1 else dataframes

    def process_data(
        self,
        data: Union[pd.DataFrame, List[pd.DataFrame]],
        process_func: Callable[..., Any],
        **kwargs: Any
    ) -> Any:
        try:
            result = process_func(data, **kwargs)
            log_and_print("✅ Data processing completed successfully")
            return result
        except Exception as e:
            log_and_print(f"❌ Error processing data: {e}")
            raise

    def save_results(
        self,
        data: Any,
        output_path: Union[str, Path],
        format: str = "excel",
        **kwargs: Any
    ) -> Path:
        output_path = Path(output_path)
        ensure_output_dir(output_path.parent)

        try:
            df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)

            if format.lower() == "excel":
                df.to_excel(output_path, index=False, **kwargs)
            else:
                df.to_csv(output_path, index=False, **kwargs)

            log_and_print(f"💾 Results saved to: {output_path}")
            return output_path

        except Exception as e:
            log_and_print(f"❌ Error saving results: {e}")
            raise

    def run_pipeline(
        self,
        input_paths: Union[str, Path, List[Union[str, Path]]],
        process_func: Callable[..., Any],
        output_path: Union[str, Path],
        required_columns: Optional[List[str]] = None,
        format: str = "excel",
        **kwargs: Any
    ) -> Tuple[Any, Path]:
        log_and_print(f"🚀 Starting {self.name} pipeline")

        data = self.load_and_validate(input_paths, required_columns)
        result = self.process_data(data, process_func, **kwargs)
        saved_path = self.save_results(result, output_path, format)

        log_and_print(f"✅ {self.name} pipeline completed successfully")

        return result, saved_path


# ─────────────────────────────────────────────────────────────
# Public API (SINGLE SOURCE OF TRUTH)
# ─────────────────────────────────────────────────────────────

def load_and_process_data(
    input_paths: Union[str, Path, List[Union[str, Path]]],
    process_func: Callable[..., Any],
    output_path: Union[str, Path],
    required_columns: Optional[List[str]] = None,
    format: str = "excel",
    **kwargs: Any
) -> Tuple[Any, Path]:
    processor = DataProcessor("DataProcessor")

    return processor.run_pipeline(
        input_paths,
        process_func,
        output_path,
        required_columns,
        format,
        **kwargs,
    )


def validate_and_transform_data(
    data: pd.DataFrame,
    validation_rules: Dict[str, Any],
    transform_func: Optional[Callable[..., Any]] = None,
    **kwargs: Any
) -> pd.DataFrame:
    for rule_name, rule_config in validation_rules.items():
        if rule_config.get("required_columns"):
            missing = set(rule_config["required_columns"]) - set(data.columns)
            if missing:
                log_and_print(
                    f"❌ Validation failed for {rule_name}: missing columns {missing}"
                )
                raise ValueError(f"Missing required columns: {missing}")

    if transform_func:
        data = transform_func(data, **kwargs)
        log_and_print("✅ Data transformation completed")

    return data


def batch_process_files(
    input_dir: Union[str, Path],
    process_func: Callable[..., Any],
    output_dir: Union[str, Path],
    file_pattern: str = "*.csv",
    **kwargs: Any
) -> List[Path]:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_files = list(input_dir.glob(file_pattern))
    output_files = []

    log_and_print(f"🔄 Processing {len(input_files)} files from {input_dir}")

    for input_file in input_files:
        try:
            output_file = output_dir / f"processed_{input_file.name}"

            _, saved_path = load_and_process_data(
                input_file,
                process_func,
                output_file,
                **kwargs,
            )

            output_files.append(saved_path)

        except Exception as e:
            log_and_print(f"❌ Error processing {input_file}: {e}")

    log_and_print(f"✅ Batch processing completed: {len(output_files)} files processed")

    return output_files