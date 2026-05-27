"""DataContentComparer tool implementation (level_1)."""

from pathlib import Path
from typing import Any, Optional, Union

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import run_mode_dispatch
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import resolve_log_dir, setup_file_logging
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import MODE_REGISTRY


class DataContentComparer(BaseTool):
  """Tool for comparing content between datasets."""

  def __init__(self) -> None:
    super().__init__(
      name="Data Content Comparer",
      description="Compares content between datasets and generates detailed reports",
      tool_name="data_content_comparer",
    )
    setup_file_logging(log_dir=resolve_log_dir(self.config))

  def run(
    self,
    mode: Optional[str] = None,
    input_paths: Optional[list[Union[str, Path]]] = None,
    output_dir: Optional[Union[str, Path]] = None,
    domain: Optional[str] = None,
    output_filename: Optional[str] = None,
    **kwargs: Any,
  ) -> None:
    _ = output_filename
    resolved_mode = mode or "standard"

    if resolved_mode in ["release_consistency", "release"]:
      if input_paths and len(input_paths) >= 2:
        log_and_print(f"Manual file comparison mode with {len(input_paths)} files")
      elif domain:
        log_and_print(f"Domain-based comparison for: {domain}")
      else:
        log_and_print("Processing all available domains")
    elif resolved_mode not in ("domain_old_vs_new",):
      if not self.validate_input_files(input_paths or [], required_count=2):
        raise ValueError("Need at least two input files to compare")

    log_and_print(f"Running {resolved_mode} mode...")
    run_mode_dispatch(
      self,
      mode=resolved_mode,
      registry=MODE_REGISTRY,
      input_paths=input_paths,
      output_dir=output_dir,
      domain=domain,
      default_mode="standard",
      **kwargs,
    )
