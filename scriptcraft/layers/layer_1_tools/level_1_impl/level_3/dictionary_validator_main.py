"""
Dictionary Validator Tool

Validates consistency between dataset columns and dictionary columns.
"""

from pathlib import Path

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_pypi.level_0_infra.level_1.data_loading import load_dataset_columns, load_dictionary_columns
from layers.layer_1_pypi.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_pypi.level_1_impl.level_0.compare_columns import compare_columns
from layers.layer_1_pypi.level_1_impl.level_0.main_common import create_entrypoint_main
from layers.layer_1_pypi.level_1_impl.level_2.runtime_loops import run_process_domain_for_single_pair


class DictionaryValidator(BaseTool):
    """Validates dataset columns against dictionary columns."""
    
    def __init__(self):
        super().__init__(
            name="Dictionary Validator",
            description="Validates consistency between dataset columns and dictionary columns",
            tool_name="dictionary_validator",
            requires_dictionary=True
        )
    
    def run(self, *args, **kwargs) -> None:
        """
        Run the dictionary validation process.
        
        Args:
            *args: Positional arguments (can include dataset_file, dictionary_file)
            **kwargs: Keyword arguments including:
                - dataset_file: Path to dataset file
                - dictionary_file: Path to dictionary file
                - domain: Domain to validate
                - output_dir: Output directory
        """
        dataset_file = kwargs.get("dataset_file") or (args[0] if args else None)
        dictionary_file = kwargs.get("dictionary_file") or (args[1] if len(args) > 1 else None)
        domain = kwargs.get("domain", "unknown")
        output_dir = kwargs.get("output_dir", self.default_output_dir)

        extra_kwargs = dict(kwargs)
        extra_kwargs.pop("dataset_file", None)
        extra_kwargs.pop("dictionary_file", None)
        extra_kwargs.pop("domain", None)
        extra_kwargs.pop("output_dir", None)

        run_process_domain_for_single_pair(
            self,
            dataset_file=dataset_file,
            dictionary_file=dictionary_file,
            output_dir=output_dir,
            domain=domain,
            extra_kwargs=extra_kwargs,
        )
    
    def process_domain(self, domain: str, dataset_file: Path, dictionary_file: Path, 
                      output_path: Path, **kwargs) -> None:
        """
        Validate dataset columns against dictionary columns.
        
        Args:
            domain: The domain to validate
            dataset_file: Path to dataset file
            dictionary_file: Path to dictionary file
            output_path: Not used (results are logged)
            **kwargs: Additional arguments
        """
        log_and_print(f"🔍 Validating {dataset_file.name} against {dictionary_file.name}...\n")

        # Load and compare columns
        dataset_columns = load_dataset_columns(dataset_file)
        dictionary_columns = load_dictionary_columns(dictionary_file)
        comparison = compare_columns(dataset_columns, dictionary_columns)

        # Log results
        log_and_print(f"✅ Columns in both: {len(comparison['in_both'])}")
        log_and_print(f"❌ Only in dataset ({len(comparison['only_in_dataset'])}): {comparison['only_in_dataset']}")
        log_and_print(f"❌ Only in dictionary ({len(comparison['only_in_dictionary'])}): {comparison['only_in_dictionary']}")
        log_and_print(f"🔄 Case mismatches ({len(comparison['case_mismatches'])}): {comparison['case_mismatches']}\n")


def _create_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description="🔎 Validates consistency between dataset columns and dictionary columns"
    )
    parser.add_argument("dataset_file", help="Path to dataset file")
    parser.add_argument("dictionary_file", help="Path to dictionary file")
    parser.add_argument("--domain", default="unknown", help="Domain label for logs")
    parser.add_argument("--output-dir", default="output", help="Output directory (not used)")
    return parser


main = create_entrypoint_main(
    DictionaryValidator,
    tool_name="dictionary_validator",
    description="Validates consistency between dataset columns and dictionary columns",
    parser_kind="custom",
    create_parser_func=_create_parser,
    run_style="kwargs",
)


if __name__ == "__main__":
    main() 