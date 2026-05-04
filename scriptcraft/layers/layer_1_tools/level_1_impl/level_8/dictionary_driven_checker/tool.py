"""DictionaryDrivenChecker tool implementation (level_1)."""

from pathlib import Path
from typing import Any, Optional, Union

from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_tools.level_1_impl.level_0.plugins import initialize_plugins
from layers.layer_1_tools.level_1_impl.level_7.dictionary_driven_checker.core import (
    execute_dictionary_driven_check,
)


InputPaths = list[Union[str, Path]]


class DictionaryDrivenChecker(BaseTool):
    """
    Thin tool wrapper.

    Delegates all logic to _core + runner.
    """

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
        _ = mode

        self.log_start()

        try:
            if not self.validate_input_files(input_paths or []):
                raise ValueError("❌ No input files provided")

            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)

            execute_dictionary_driven_check(
                input_paths=input_paths or [],
                output_path=output_path,
                domain=domain,
                output_filename=output_filename,
                outlier_method=kwargs.get("outlier_method", self.outlier_method),
                dictionary_path=kwargs.get("dictionary_path"),
                load_data_file=self.load_data_file,
            )

            self.log_completion()

        except Exception as e:
            self.log_error(f"Dictionary validation failed: {e}")
            raise