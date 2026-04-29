"""FunctionAuditorTool implementation (level_1)."""

from pathlib import Path
from typing import Any, Optional, Union

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_pypi.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_pypi.level_1_impl.level_0.function_auditor.types import InputPaths
from layers.layer_1_pypi.level_1_impl.level_0.function_auditor.languages import extension_for_language
from layers.layer_1_pypi.level_1_impl.level_2.function_auditor.batch_mode import run_batch_mode
from layers.layer_1_pypi.level_1_impl.level_2.function_auditor.single_file_mode import run_single_file_mode

_BATCH_MODES = {"batch", "folder", "pattern"}


class FunctionAuditorTool(BaseTool):
    """Tool for auditing unused functions in codebases."""

    def __init__(self) -> None:
        super().__init__(
            name="Function Auditor",
            description=(
                "🔍 Audits unused functions in codebases and provides cleanup recommendations"
            ),
            tool_name="function_auditor",
        )

        tool_config = self.get_tool_config()
        self.default_language = tool_config.get("default_language", "python")

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
            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)

            language = kwargs.get("language", self.default_language)
            extension = kwargs.get("extension", extension_for_language(language))
            pattern = kwargs.get("pattern")
            folder = kwargs.get("folder")
            summary_only = kwargs.get("summary_only", False)
            unused_only = kwargs.get("unused_only", False)
            detailed_unused = kwargs.get("detailed_unused", False)

            if mode == "single" or (input_paths and len(input_paths) == 1):
                run_single_file_mode(
                    file_path=input_paths[0],
                    output_path=output_path,
                )
            elif mode in _BATCH_MODES or (input_paths and len(input_paths) > 1):
                run_batch_mode(
                    input_paths=input_paths,
                    output_path=output_path,
                    language=language,
                    extension=extension,
                    pattern=pattern,
                    folder=folder,
                    summary_only=summary_only,
                    unused_only=unused_only,
                    detailed_unused=detailed_unused,
                )
            else:
                log_and_print(
                    "🔍 No specific mode specified, running batch audit on current directory"
                )
                run_batch_mode(
                    input_paths=None,
                    output_path=output_path,
                    language=language,
                    extension=extension,
                    pattern=pattern,
                    folder=folder,
                    summary_only=summary_only,
                    unused_only=unused_only,
                    detailed_unused=detailed_unused,
                )

            self.log_completion(output_path)

        except Exception as e:
            self.log_error(f"Function audit failed: {e}")
            raise
