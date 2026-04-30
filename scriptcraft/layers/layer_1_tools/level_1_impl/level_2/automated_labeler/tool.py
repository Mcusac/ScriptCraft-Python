"""AutomatedLabeler tool implementation (level_1)."""

from pathlib import Path
from typing import Any, Optional, Union

from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_tools.level_1_impl.level_0.automated_labeler.types import InputPaths, LabelingRules
from layers.layer_1_tools.level_1_impl.level_1.automated_labeler.labeling_mode import run_labeling_mode
from layers.layer_1_tools.level_1_impl.level_1.automated_labeler.template_mode import run_template_mode


class AutomatedLabeler(BaseTool):
    """Tool for automated data labeling and document template filling."""

    def __init__(self) -> None:
        super().__init__(
            name="Automated Labeler",
            description="🏷️ Automatically generates labels and fills document templates with data",
            tool_name="automated_labeler",
        )

        tool_config = self.get_tool_config()
        self.sets_per_page = tool_config.get("sets_per_page", 8)

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

            labeling_rules: LabelingRules = kwargs.get("labeling_rules", {})
            output_format = kwargs.get("output_format", "excel")
            template_path = kwargs.get("template_path")

            if mode == "template" or template_path:
                run_template_mode(
                    tool=self,
                    input_paths=input_paths or [],
                    output_path=output_path,
                    template_path=template_path,
                    output_filename=output_filename,
                    sets_per_page=self.sets_per_page,
                )
            else:
                run_labeling_mode(
                    tool=self,
                    input_paths=input_paths or [],
                    output_path=output_path,
                    domain=domain,
                    labeling_rules=labeling_rules,
                    output_format=output_format,
                    output_filename=output_filename,
                )

            self.log_completion()
        except Exception as e:
            self.log_error(f"Error: {str(e)}")
            raise

