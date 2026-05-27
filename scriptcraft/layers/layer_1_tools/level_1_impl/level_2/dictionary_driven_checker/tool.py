"""DictionaryDrivenChecker tool implementation (level_1)."""

from pathlib import Path
from typing import Any, Optional, Union

from scriptcraft.layers.layer_0_core.level_0 import InputPaths

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import run_tool_lifecycle
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import initialize_plugins
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import execute_dictionary_driven_check


class DictionaryDrivenChecker(BaseTool):
  """Thin tool wrapper delegating to shared dictionary check orchestration."""

  def __init__(self) -> None:
    super().__init__(
      name="Dictionary Driven Checker",
      description="Validates data against a data dictionary using configurable plugins",
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

    def _work() -> None:
      if not self.validate_input_files(input_paths or []):
        raise ValueError("No input files provided")
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

    run_tool_lifecycle(self, work=_work, output_dir=output_dir)
