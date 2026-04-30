"""DictionaryDrivenChecker tool implementation (level_1)."""

from pathlib import Path
from typing import Any, Optional, Union

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_0.paths import OutlierMethod
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_tools.level_1_impl.level_0.plugins import initialize_plugins
from layers.layer_1_tools.level_1_impl.level_0.dictionary_driven_checker import run_dictionary_checker

from layers.layer_1_tools.level_1_impl.level_0.dictionary_driven_checker.dictionary_finder import find_dictionary_file
from layers.layer_1_tools.level_1_impl.level_6.dictionary_driven_checker.normalization import ensure_dataframe, normalize_dataset_columns, normalize_dictionary_df

InputPaths = list[Union[str, Path]]


class DictionaryDrivenChecker(BaseTool):
    """Tool for validating data against a data dictionary using plugins."""

    def __init__(self) -> None:
        super().__init__(
            name="Dictionary Driven Checker",
            description="🔍 Validates data against a data dictionary using configurable plugins",
            tool_name="dictionary_driven_checker",
        )

        tool_config = self.get_tool_config()
        self.outlier_method = tool_config.get("outlier_detection", "IQR")

        initialize_plugins(self.config)

    def run(
        self,
        mode: Optional[str] = None,
        input_paths: Optional[InputPaths] = None,
        output_dir: Optional[Union[str, Path]] = None,
        domain: Optional[str] = None,
        output_filename: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        _ = mode  # reserved for future modes; argparse may still pass it

        self.log_start()
        try:
            if not self.validate_input_files(input_paths or []):
                raise ValueError("❌ No input files provided")

            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)

            outlier_method = kwargs.get("outlier_method", self.outlier_method)
            dictionary_path = kwargs.get("dictionary_path")

            for input_path in input_paths or []:
                log_and_print(f"🔍 Validating: {input_path}")

                data = ensure_dataframe(self.load_data_file(input_path), label="dataset")
                data = normalize_dataset_columns(data)

                if dictionary_path:
                    dict_path = Path(dictionary_path)
                else:
                    dict_path = find_dictionary_file(input_path, domain)

                if not dict_path.exists():
                    raise FileNotFoundError(f"Dictionary not found: {dict_path}")

                log_and_print(f"📂 Loading dictionary: {dict_path}")
                dict_df = ensure_dataframe(self.load_data_file(dict_path), label="dictionary")
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

            self.log_completion()
        except Exception as e:
            self.log_error(f"Dictionary validation failed: {e}")
            raise

