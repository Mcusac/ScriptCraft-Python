"""
Feature Change Checker Tool

Tracks and categorizes changes in feature values between visits or timepoints.
"""

from pathlib import Path
from typing import Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.process_domain_mixins import DomainFileToolMixin
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1.data_loading import load_data
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.runtime_loops import run_process_domain_over_input_paths
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7.base_tool import BaseTool

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.feature_change_checker import (
    run_categorized_changes,
    run_between_visit_changes,
)



class FeatureChangeChecker(BaseTool, DomainFileToolMixin):
    """
    Checker for tracking changes in feature values between visits.

    This tool follows DomainFileToolMixin:
    - dataset_file is required
    - dictionary_file is ignored but present for interface consistency
    """

    def __init__(self, feature_name: str = "CDX_Cog", categorize: bool = True):
        super().__init__(
            name="Feature Change Checker",
            description=f"Tracks changes in {feature_name} values between visits",
            tool_name="feature_change_checker"
        )
        self.feature_name = feature_name
        self.categorize = categorize

    # -----------------------------
    # Run orchestration (unchanged)
    # -----------------------------
    def run(self, *args, **kwargs) -> None:
        input_paths = kwargs.get("input_paths") or (args[0] if args else None)
        output_dir = kwargs.get("output_dir", self.default_output_dir)
        domain = kwargs.get("domain", "unknown")

        feature_name = kwargs.get("feature_name", self.feature_name)
        categorize = kwargs.get("categorize", self.categorize)

        extra_kwargs = dict(kwargs)
        extra_kwargs.pop("input_paths", None)
        extra_kwargs.pop("output_dir", None)
        extra_kwargs.pop("domain", None)

        extra_kwargs["feature_name"] = feature_name
        extra_kwargs["categorize"] = categorize

        run_process_domain_over_input_paths(
            self,
            input_paths=input_paths,
            output_dir=output_dir,
            domain=domain,
            dictionary_file=None,
            extra_kwargs=extra_kwargs,
        )

    # -----------------------------
    # Mixin-required implementation
    # -----------------------------
    def _process_domain_impl(
        self,
        domain: str,
        dataset_file: Path,
        dictionary_file: Optional[Path],
        output_path: Path,
        **kwargs
    ) -> None:

        log_and_print(
            f"🔍 Checking feature changes for '{self.feature_name}' in {domain}..."
        )

        # Explicitly enforce intended data access pattern
        df = load_data(dataset_file)

        if self.feature_name not in df.columns:
            log_and_print(
                f"❌ Feature '{self.feature_name}' not found in dataset",
                level="error"
            )
            return

        if self.categorize:
            run_categorized_changes(df, self.feature_name, output_path)
        else:
            run_between_visit_changes(df, self.feature_name, output_path)

        log_and_print(f"✅ Feature change analysis completed for {domain}")