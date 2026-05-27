"""FunctionAuditorTool implementation (level_1)."""

from pathlib import Path
from typing import Any, Optional, Union

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import InputPaths, extension_for_language, log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import run_tool_lifecycle
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import run_single_file_mode
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import run_batch_mode
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool

_BATCH_MODES = {"batch", "folder", "pattern"}


class FunctionAuditorTool(BaseTool):
  """Tool for auditing unused functions in codebases."""

  def __init__(self) -> None:
    super().__init__(
      name="Function Auditor",
      description="Audits unused functions in codebases and provides cleanup recommendations",
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
    _ = domain, output_filename
    language = kwargs.get("language", self.default_language)
    extension = kwargs.get("extension", extension_for_language(language))
    pattern = kwargs.get("pattern")
    folder = kwargs.get("folder")
    summary_only = kwargs.get("summary_only", False)
    unused_only = kwargs.get("unused_only", False)
    detailed_unused = kwargs.get("detailed_unused", False)

    def _work() -> None:
      output_path = self.resolve_output_directory(output_dir or self.default_output_dir)
      if mode == "single" or (input_paths and len(input_paths) == 1):
        run_single_file_mode(file_path=input_paths[0], output_path=output_path)
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
        log_and_print("No specific mode specified, running batch audit on current directory")
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

    run_tool_lifecycle(self, work=_work, output_dir=output_dir)
