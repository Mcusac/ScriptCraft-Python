"""
Feature Change Checker Tool

Tracks and categorizes changes in feature values between visits or timepoints.
"""

from pathlib import Path
from typing import Optional

from scriptcraft.layers.layer_0_core.level_1 import (
    run_process_domain_over_input_paths,
    build_run_context
)
from scriptcraft.layers.layer_0_core.level_5 import load_tabular

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import DomainFileToolMixin, log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import run_between_visit_changes
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool, run_categorized_changes


class FeatureChangeChecker(BaseTool, DomainFileToolMixin):
  """Checker for tracking changes in feature values between visits."""

  def __init__(self, feature_name: str = "CDX_Cog", categorize: bool = True):
    super().__init__(
      name="Feature Change Checker",
      description=f"Tracks changes in {feature_name} values between visits",
      tool_name="feature_change_checker",
    )
    self.feature_name = feature_name
    self.categorize = categorize

  def run(self, *args, **kwargs) -> None:
    ctx = build_run_context(*args, **kwargs)
    ctx.extra_kwargs.setdefault("feature_name", kwargs.get("feature_name", self.feature_name))
    ctx.extra_kwargs.setdefault("categorize", kwargs.get("categorize", self.categorize))
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
    dictionary_file: Optional[Path],
    output_path: Path,
    **kwargs,
  ) -> None:
    _ = dictionary_file
    feature_name = kwargs.get("feature_name", self.feature_name)
    categorize = kwargs.get("categorize", self.categorize)

    log_and_print(f"Checking feature changes for '{feature_name}' in {domain}...")
    df = load_tabular(dataset_file)
    if feature_name not in df.columns:
      log_and_print(f"Feature '{feature_name}' not found in dataset", level="error")
      return

    if categorize:
      run_categorized_changes(df, feature_name, output_path)
    else:
      run_between_visit_changes(df, feature_name, output_path)

    log_and_print(f"Feature change analysis completed for {domain}")
