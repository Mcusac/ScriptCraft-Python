"""
Dictionary Validator Tool

Validates consistency between dataset columns and dictionary columns.
"""

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.process_domain_mixins import DomainFileToolMixin
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1.data_loading import (
    load_dataset_columns,
    load_dictionary_columns
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.runtime_loops import run_process_domain_for_single_pair
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7.base_tool import BaseTool

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.compare_columns import compare_columns
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.main_common import create_entrypoint_main


class DictionaryValidator(BaseTool, DomainFileToolMixin):
    """
    Validates dataset columns against dictionary columns.

    This tool follows DomainFileToolMixin:
    - dataset_file is required
    - dictionary_file is required
    - both are explicitly used
    """

    def __init__(self):
        super().__init__(
            name="Dictionary Validator",
            description="Validates consistency between dataset columns and dictionary columns",
            tool_name="dictionary_validator",
            requires_dictionary=True
        )

    # -----------------------------
    # Run (unchanged orchestration)
    # -----------------------------
    def run(self, *args, **kwargs) -> None:
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

    # -----------------------------
    # Mixin-required implementation
    # -----------------------------
    def _process_domain_impl(
        self,
        domain: str,
        dataset_file: Path,
        dictionary_file: Path,
        output_path: Path,
        **kwargs
    ) -> None:

        log_and_print(
            f"🔍 Validating {dataset_file.name} against {dictionary_file.name}..."
        )

        # Load inputs (consistent infra usage enforced by mixin design intent)
        dataset_columns = load_dataset_columns(dataset_file)
        dictionary_columns = load_dictionary_columns(dictionary_file)

        comparison = compare_columns(dataset_columns, dictionary_columns)

        log_and_print(f"✅ Columns in both: {len(comparison['in_both'])}")
        log_and_print(
            f"❌ Only in dataset ({len(comparison['only_in_dataset'])}): "
            f"{comparison['only_in_dataset']}"
        )
        log_and_print(
            f"❌ Only in dictionary ({len(comparison['only_in_dictionary'])}): "
            f"{comparison['only_in_dictionary']}"
        )
        log_and_print(
            f"🔄 Case mismatches ({len(comparison['case_mismatches'])}): "
            f"{comparison['case_mismatches']}\n"
        )


# -----------------------------
# CLI unchanged
# -----------------------------
def _create_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description="🔎 Validates consistency between dataset columns and dictionary columns"
    )
    parser.add_argument("dataset_file")
    parser.add_argument("dictionary_file")
    parser.add_argument("--domain", default="unknown")
    parser.add_argument("--output-dir", default="output")
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