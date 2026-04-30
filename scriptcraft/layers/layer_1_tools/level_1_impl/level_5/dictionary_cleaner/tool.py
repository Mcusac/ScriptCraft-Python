"""DictionaryCleaner tool implementation (level_1)."""

from pathlib import Path
from typing import Any, Optional, Union

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from .normalizer import clean_dictionary
from .types import InputPaths


class DictionaryCleaner(BaseTool):
    """Tool for cleaning and standardizing data dictionary entries."""

    def __init__(self) -> None:
        super().__init__(
            name="Dictionary Cleaner",
            description=(
                "🧹 Cleans and standardizes data dictionary entries including value types "
                "and expected values"
            ),
            tool_name="dictionary_cleaner",
            supported_formats=[".csv", ".xlsx", ".xls"],
        )

    def run(
        self,
        mode: Optional[str] = None,
        input_paths: Optional[InputPaths] = None,
        output_dir: Optional[Union[Path, str]] = None,
        domain: Optional[str] = None,
        output_filename: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.log_start()
        try:
            if not self.validate_input_files(input_paths or []):
                raise ValueError("❌ No input files provided")

            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)

            cleaning_level = kwargs.get("cleaning_level", "standard")
            explicit_filename = output_filename

            for input_path in input_paths or []:
                log_and_print(f"🧹 Processing dictionary: {input_path}")

                data = self.load_data_file(input_path)

                log_and_print(f"🔄 Cleaning dictionary for {domain or 'dataset'}...")
                cleaned_data = clean_dictionary(data, cleaning_level=cleaning_level)

                resolved_filename = explicit_filename or self.get_output_filename(
                    input_path, suffix="cleaned"
                )
                output_file = output_path / resolved_filename

                self.save_data_file(cleaned_data, output_file, include_index=False)
                log_and_print(f"✅ Dictionary cleaning completed: {output_file}")

            self.log_completion()

        except Exception as e:
            self.log_error(f"Dictionary cleaning failed: {e}")
            raise
