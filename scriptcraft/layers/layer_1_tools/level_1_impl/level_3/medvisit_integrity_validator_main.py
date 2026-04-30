"""
MedVisit Integrity Validator Tool

This validator checks Med_ID and Visit_ID integrity between old and new datasets.
"""

import pandas as pd

import argparse

from pathlib import Path
from typing import Optional, Dict

from layers.layer_1_tools.level_0_infra.level_0.directory_ops import ensure_output_dir
from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_datasets
from layers.layer_1_tools.level_0_infra.level_1.cleaning import standardize_columns
from layers.layer_1_tools.level_0_infra.level_1.comparison import compare_dataframes
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_tools.level_1_impl.level_0.main_common import create_entrypoint_main
from layers.layer_1_tools.level_1_impl.level_2.runtime_loops import run_domains

# File mapping for different domains
FILENAME_MAP: Dict[str, Dict[str, str]] = {
    "Biomarkers": {
        "old": "HD Release 6 Biomarkers_FINAL.csv",
        "new": "HD6 + New data_Biomarkers---MatthewReviewPending.xlsx"
    },
    # "Clinical": {
    #     "old": "HD Release 6 Clinical_FINAL.csv",
    #     "new": "HD6 + New data_Clinical---Review.xlsx"
    # },
    # Add Genomics/Imaging when ready
}


class MedVisitIntegrityValidator(BaseTool):
    """Validator for checking Med_ID and Visit_ID integrity between old and new datasets."""
    
    def __init__(self):
        super().__init__(
            name="MedVisit Integrity Validator",
            description="Validates the integrity of Med_ID and Visit_ID combinations between datasets",
            tool_name="medvisit_integrity_validator"
        )
    
    def run(self, *args, **kwargs) -> None:
        """
        Run the MedVisit integrity validation process.
        
        Args:
            *args: Positional arguments (can include domains)
            **kwargs: Keyword arguments including:
                - domains: List of domains to process
                - output_dir: Output directory
        """
        domains = kwargs.get("domains") or (args[0] if args else None)
        output_dir = kwargs.get("output_dir", self.default_output_dir)

        extra_kwargs = dict(kwargs)
        extra_kwargs.pop("domains", None)
        extra_kwargs.pop("output_dir", None)

        def _per_domain(domain: str, output_path: Path) -> None:
            if domain not in FILENAME_MAP:
                log_and_print(f"⚠️ Skipping {domain} — no file mapping found.")
                return

            log_and_print(f"🔍 Processing domain: {domain}")
            domain_output = output_path / f"{domain}_medvisit_integrity.xlsx"
            self.process_domain(domain, None, None, domain_output, **extra_kwargs)

        run_domains(
            self,
            domains=domains,
            default_domains=list(FILENAME_MAP.keys()),
            output_dir=output_dir,
            per_domain_callable=_per_domain,
        )
    
    def process_domain(self, domain: str, dataset_file: Path, dictionary_file: Optional[Path], 
                      output_path: Path, **kwargs) -> None:
        """
        Validate Med_ID and Visit_ID integrity between old and new datasets.
        
        Args:
            domain: The domain to validate (e.g., "Biomarkers", "Clinical")
            dataset_file: Not used in this validator
            dictionary_file: Not used in this validator
            output_path: Path to save the validation results
            **kwargs: Additional arguments
        """
        filenames = FILENAME_MAP.get(domain)
        if not filenames:
            log_and_print(f"⏩ Skipping {domain} — no file mapping found.")
            return

        log_and_print(f"🔍 Validating Med/Visit ID integrity for {domain}...")

        df_old, df_new = load_datasets(
            old_filename=filenames["old"],
            new_filename=filenames["new"],
            data_dir=domain,
            mode="standard"
        )

        df_new = standardize_columns(df_new, {"Visit": "Visit_ID", "Med ID": "Med_ID"})
        
        # Use compare_dataframes with med_ids step to check Med/Visit ID integrity
        comparison_result = compare_dataframes(
            df_old, 
            df_new, 
            dataset_name=domain,
            steps=["med_ids"]
        )
        
        # Extract missing IDs from the comparison result
        missing_in_new, missing_in_old = comparison_result.missing_ids or (pd.DataFrame(), pd.DataFrame())

        ensure_output_dir(output_path)
        with pd.ExcelWriter(output_path) as writer:
            missing_in_new.to_excel(writer, sheet_name="Missing in New", index=False)
            missing_in_old.to_excel(writer, sheet_name="Missing in Old", index=False)

        log_and_print(f"🔍 Combos missing in new dataset: {len(missing_in_new)}")
        log_and_print(f"🔍 Combos missing in old dataset: {len(missing_in_old)}")
        log_and_print(f"✅ Comparison saved to: {output_path}")


def main():
    """Main entry point for the medvisit integrity validator tool."""
    def _create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Validates the integrity of Med_ID and Visit_ID combinations between datasets"
        )
        parser.add_argument(
            "--domains",
            nargs="+",
            help="Domains to validate (default: all mapped domains)",
        )
        parser.add_argument(
            "--output-dir",
            default="output",
            help="Output directory (default: output)",
        )
        return parser

    def _run_kwargs(args: argparse.Namespace) -> Dict[str, object]:
        return {
            "domains": args.domains,
            "output_dir": args.output_dir,
        }

    create_entrypoint_main(
        MedVisitIntegrityValidator,
        tool_name="medvisit_integrity_validator",
        description="Validates the integrity of Med_ID and Visit_ID combinations between datasets",
        parser_kind="custom",
        create_parser_func=_create_parser,
        run_kwargs_builder=_run_kwargs,
    )()


if __name__ == "__main__":
    main() 