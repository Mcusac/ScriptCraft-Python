"""
Score Totals Checker Tool

This checker validates that calculated totals match expected totals in datasets.
"""

from pathlib import Path
from typing import Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_data

from layers.layer_1_tools.level_1_impl.level_0.score_totals_checker import calculate_totals_and_compare
from layers.layer_1_tools.level_1_impl.level_0.main_common import create_entrypoint_main
from layers.layer_1_tools.level_1_impl.level_2.runtime_loops import run_process_domain_over_input_paths


class ScoreTotalsChecker(BaseTool):
    """Checker for validating that calculated totals match expected totals in datasets."""
    
    def __init__(self):
        super().__init__(
            name="Score Totals Checker",
            description="Validates that calculated totals match expected totals in datasets",
            tool_name="score_totals_checker"
        )
    
    def run(self, *args, **kwargs) -> None:
        """
        Run the score totals checking process.
        
        Args:
            *args: Positional arguments (can include input_paths, domain)
            **kwargs: Keyword arguments including:
                - input_paths: List of input file paths
                - output_dir: Output directory
                - domain: Domain to process
        """
        input_paths = kwargs.get("input_paths") or (args[0] if args else None)
        output_dir = kwargs.get("output_dir", self.default_output_dir)
        domain = kwargs.get("domain", "unknown")

        extra_kwargs = dict(kwargs)
        extra_kwargs.pop("input_paths", None)
        extra_kwargs.pop("output_dir", None)
        extra_kwargs.pop("domain", None)

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
        Check calculated totals against expected totals.
        
        Args:
            domain: The domain to check
            dataset_file: Path to dataset file
            dictionary_file: Not used for this tool
            output_path: Path to save results
            **kwargs: Additional arguments
        """
        log_and_print(f"🔍 Checking totals in {dataset_file.name} for {domain}...")

        try:
            # Load data
            df = load_data(dataset_file)
            
            # Calculate totals and compare
            results = calculate_totals_and_compare(df, domain)
            
            # Save results
            if not results.empty:
                output_file = output_path / f"{domain}_totals_check.csv"
                results.to_csv(output_file, index=False)
                log_and_print(f"✅ Results saved to: {output_file}")
            else:
                log_and_print(f"⚠️ No total columns found to check in {domain}")
                
        except Exception as e:
            log_and_print(f"❌ Error checking totals for {domain}: {e}", level="error")
            raise


main = create_entrypoint_main(
    ScoreTotalsChecker,
    tool_name="score_totals_checker",
    description="Validates that calculated totals match expected totals in datasets",
    parser_kind="standard",
)


if __name__ == "__main__":
    main() 