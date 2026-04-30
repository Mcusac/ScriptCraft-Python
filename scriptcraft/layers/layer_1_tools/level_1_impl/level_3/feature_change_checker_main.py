"""
Feature Change Checker Tool

Tracks and categorizes changes in feature values between visits or timepoints.
"""

from pathlib import Path
from typing import Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_data
from layers.layer_1_tools.level_0_infra.level_6.argument_parsers import ParserFactory
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_tools.level_1_impl.level_0.feature_change_checker import (
    run_categorized_changes,
    run_between_visit_changes,
)
from layers.layer_1_tools.level_1_impl.level_2.runtime_loops import run_process_domain_over_input_paths


class FeatureChangeChecker(BaseTool):
    """Checker for tracking changes in feature values between visits."""
    
    def __init__(self, feature_name: str = "CDX_Cog", categorize: bool = True):
        """
        Initialize the feature change checker.
        
        Args:
            feature_name: Name of the feature to track changes for
            categorize: Whether to categorize changes or just track differences
        """
        super().__init__(
            name="Feature Change Checker",
            description=f"Tracks changes in {feature_name} values between visits",
            tool_name="feature_change_checker"
        )
        self.feature_name = feature_name
        self.categorize = categorize
    
    def run(self, *args, **kwargs) -> None:
        """
        Run the feature change checking process.
        
        Args:
            *args: Positional arguments (can include dataset_file, domain)
            **kwargs: Keyword arguments including:
                - input_paths: List of input file paths
                - output_dir: Output directory
                - domain: Domain to process
                - feature_name: Name of feature to track
                - categorize: Whether to categorize changes
        """
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
    
    def process_domain(self, domain: str, dataset_file: Path, dictionary_file: Optional[Path], 
                      output_path: Path, **kwargs) -> None:
        """
        Check feature changes between visits.
        
        Args:
            domain: The domain to check (e.g., "Biomarkers", "Clinical")
            dataset_file: Path to dataset file
            dictionary_file: Not used for this tool
            output_path: Path to output directory
            **kwargs: Additional arguments
        """
        log_and_print(f"🔍 Checking feature changes for '{self.feature_name}' in {domain}...")
        
        # Load data
        df = load_data(dataset_file)
        
        if self.feature_name not in df.columns:
            log_and_print(f"❌ Feature '{self.feature_name}' not found in dataset", level="error")
            return
        
        # Run analysis based on configuration
        if self.categorize:
            run_categorized_changes(df, self.feature_name, output_path)
        else:
            run_between_visit_changes(df, self.feature_name, output_path)
        
        log_and_print(f"✅ Feature change analysis completed for {domain}")


def main():
    """Main entry point for the feature change checker tool."""
    parser = ParserFactory.create_standard_tool_parser(
        "feature_change_checker",
        "Tracks and categorizes changes in feature values between visits",
    )
    parser.add_argument(
        "--feature-name",
        default="CDX_Cog",
        help="Feature column name to track (default: CDX_Cog)",
    )
    parser.add_argument(
        "--categorize",
        action="store_true",
        default=True,
        help="Categorize changes (default: True)",
    )
    parser.add_argument(
        "--no-categorize",
        action="store_false",
        dest="categorize",
        help="Disable categorization (track raw differences only)",
    )

    args = parser.parse_args()

    tool = FeatureChangeChecker(feature_name=args.feature_name, categorize=args.categorize)
    tool.run(
        input_paths=args.input_paths,
        output_dir=args.output_dir,
        domain=args.domain,
        output_filename=args.output_filename,
        mode=args.mode,
        feature_name=args.feature_name,
        categorize=args.categorize,
    )


if __name__ == "__main__":
    main() 