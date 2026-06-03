"""DateFormatStandardizer tool implementation (level_3)."""

from pathlib import Path
from typing import Any, Optional, Union

from scriptcraft.layers.layer_0_core.level_0 import is_date_column, standardize_date_column

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool


class DateFormatStandardizer(BaseTool):
    """Tool for standardizing date formats in datasets."""

    def __init__(self) -> None:
        super().__init__(
            name="Date Format Standardizer",
            description="📅 Standardizes date formats in datasets to ensure consistency",
            tool_name="date_format_standardizer",
        )

    def run(
        self,
        input_paths: Optional[list[Union[str, Path]]] = None,
        output_dir: Optional[Union[str, Path]] = None,
        domain: Optional[str] = None,
        output_filename: Optional[str] = None,
        **kwargs: Any,
    ) -> bool:
        self.log_start()

        try:
            if not self.validate_input_files(input_paths or []):
                raise ValueError("❌ No input files provided")

            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)

            for input_path in input_paths or []:
                log_and_print(f"📅 Processing: {input_path}")

                data = self.load_data_file(input_path)

                log_and_print(f"🔄 Standardizing date formats for {domain or 'dataset'}...")
                transformed_data = self._standardize_dates(data)

                resolved_output_filename = output_filename or self.get_output_filename(
                    input_path,
                    suffix="date_standardized",
                )

                output_file = output_path / resolved_output_filename
                self.save_data_file(transformed_data, output_file, include_index=False)

                log_and_print(f"✅ Date standardization completed: {output_file}")

            self.log_completion()
            return True
        except Exception as e:
            self.log_error(f"Date format standardization failed: {e}")
            return False

    def _standardize_dates(self, data: Any) -> Any:
        if not hasattr(data, "columns"):
            return data

        standardized = data.copy()
        for col in standardized.columns:
            is_date = is_date_column(data[col])
            log_and_print(
                f"📅 Column '{col}' detected as {'date' if is_date else 'non-date'} column."
            )
            if not is_date:
                log_and_print(
                    f"ℹ️ Column '{col}' did not meet date detection threshold. Skipping."
                )
                continue

            log_and_print(f"📅 Standardizing date column: {col}")
            try:
                standardized[col] = standardize_date_column(data[col])
            except Exception as e:
                log_and_print(f"❌ Failed to standardize date column '{col}': {e}")

        return standardized

