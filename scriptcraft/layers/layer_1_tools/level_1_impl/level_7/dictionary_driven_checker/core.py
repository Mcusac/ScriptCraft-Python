from pathlib import Path
from typing import Any, Optional, Union

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_0.constants import OutlierMethod

from layers.layer_1_tools.level_1_impl.level_1.dictionary_driven_checker.runner import run_dictionary_checker
from layers.layer_1_tools.level_1_impl.level_0.dictionary_driven_checker.dictionary_finder import find_dictionary_file
from layers.layer_1_tools.level_1_impl.level_6.dictionary_driven_checker.normalization import (
    ensure_dataframe,
    normalize_dataset_columns,
    normalize_dictionary_df,
)


InputPaths = list[Union[str, Path]]


def execute_dictionary_driven_check(
    *,
    input_paths: InputPaths,
    output_path: Path,
    domain: Optional[str],
    output_filename: Optional[str],
    outlier_method: str,
    dictionary_path: Optional[str],
    load_data_file: Any,
) -> None:
    """
    Shared orchestration logic for DictionaryDrivenChecker tool.

    Fully reusable across all tool entrypoints.
    """

    for input_path in input_paths:
        log_and_print(f"🔍 Validating: {input_path}")

        data = ensure_dataframe(load_data_file(input_path), label="dataset")
        data = normalize_dataset_columns(data)

        dict_path = (
            Path(dictionary_path)
            if dictionary_path
            else find_dictionary_file(input_path, domain)
        )

        if not dict_path.exists():
            raise FileNotFoundError(f"Dictionary not found: {dict_path}")

        log_and_print(f"📂 Loading dictionary: {dict_path}")
        dict_df = ensure_dataframe(load_data_file(dict_path), label="dictionary")
        dict_df = normalize_dictionary_df(dict_df)

        log_and_print(f"🔄 Running validation for {domain or 'dataset'}...")

        run_dictionary_checker(
            df=data,
            dict_df=dict_df,
            domain=domain or "unknown",
            output_path=output_path,
            outlier_method=OutlierMethod[str(outlier_method).upper()],
            output_filename=output_filename,
        )

        log_and_print(f"✅ Validation completed: {output_path}")