"""
Schema Detector Tool

Automatically detects and generates database schemas from datasets.
"""

from pathlib import Path
from typing import List

from scriptcraft.layers.layer_0_core.level_1 import (
    run_process_domain_over_input_paths,
    build_run_context
)

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import EngineWrapperToolMixin, log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import SchemaDetector


class SchemaDetectorTool(EngineWrapperToolMixin, BaseTool):
  """Schema detection tool for datasets."""

  def __init__(self):
    super().__init__(
      name="Schema Detector",
      description="Analyzes datasets and generates database schemas",
      tool_name="schema_detector",
    )
    self.detector = SchemaDetector()

  def run(self, *args, **kwargs) -> None:
    ctx = build_run_context(*args, **kwargs)
    run_process_domain_over_input_paths(
      self,
      input_paths=ctx.input_paths,
      output_dir=ctx.output_dir,
      domain=ctx.domain,
      dictionary_file=None,
      extra_kwargs=ctx.extra_kwargs,
    )

  def _process_domain_impl(
    self,
    domain: str,
    dataset_file: Path,
    output_path: Path,
    **kwargs,
  ) -> None:
    log_and_print(f"Analyzing schema for {domain}: {dataset_file.name}")
    success = self.detector.run(
      input_paths=[str(dataset_file)],
      output_dir=str(output_path),
      target_database=kwargs.get("target_database", "sqlite"),
      privacy_mode=kwargs.get("privacy_mode", True),
      sample_size=kwargs.get("sample_size", 1000),
      naming_convention=kwargs.get("naming_convention", "pascal_case"),
      output_formats=kwargs.get("output_formats", ["sql", "json", "yaml"]),
    )
    if not success:
      raise RuntimeError(f"Schema detection failed for {domain}")

  def run_standalone(
    self,
    input_files: List[str],
    output_dir: str = "output",
    target_database: str = "sqlite",
    **kwargs,
  ) -> bool:
    log_and_print(f"Starting standalone schema detection for {len(input_files)} file(s)")
    return self.detector.run(
      input_paths=input_files,
      output_dir=output_dir,
      target_database=target_database,
      privacy_mode=True,
      **kwargs,
    )
