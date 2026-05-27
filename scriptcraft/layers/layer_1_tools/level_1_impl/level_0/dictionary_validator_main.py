"""
Dictionary Validator Tool

Validates consistency between dataset columns and dictionary columns.
"""

import argparse

from pathlib import Path

from scriptcraft.layers.layer_0_core.level_1 import (
    run_process_domain_for_single_pair,
    build_run_context
)
from scriptcraft.layers.layer_0_core.level_5 import load_tabular

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import DomainFileToolMixin, log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import compare_column_sets
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main, BaseTool


class DictionaryValidator(BaseTool, DomainFileToolMixin):
  """Validates dataset columns against dictionary columns."""

  def __init__(self):
    super().__init__(
      name="Dictionary Validator",
      description="Validates consistency between dataset columns and dictionary columns",
      tool_name="dictionary_validator",
      requires_dictionary=True,
    )

  def run(self, *args, **kwargs) -> None:
    ctx = build_run_context(*args, **kwargs)
    run_process_domain_for_single_pair(
      self,
      dataset_file=ctx.dataset_file,
      dictionary_file=ctx.dictionary_file,
      output_dir=ctx.output_dir,
      domain=ctx.domain,
      extra_kwargs=ctx.extra_kwargs,
    )

  def _process_domain_impl(
    self,
    domain: str,
    dataset_file: Path,
    dictionary_file: Path,
    output_path: Path,
    **kwargs,
  ) -> None:
    _ = domain, output_path, kwargs
    log_and_print(f"Validating {dataset_file.name} against {dictionary_file.name}...")
    dataset_columns = list(load_tabular(dataset_file).columns)
    dictionary_columns = list(load_tabular(dictionary_file).columns)
    comparison = compare_column_sets(dataset_columns, dictionary_columns)
    log_and_print(f"Columns in both: {len(comparison['in_both'])}")
    log_and_print(f"Only in dataset ({len(comparison['only_in_dataset'])}): {comparison['only_in_dataset']}")
    log_and_print(
      f"Only in dictionary ({len(comparison['only_in_dictionary'])}): {comparison['only_in_dictionary']}"
    )
    log_and_print(f"Case mismatches ({len(comparison['case_mismatches'])}): {comparison['case_mismatches']}\n")


def _create_parser():
  parser = argparse.ArgumentParser(
    description="Validates consistency between dataset columns and dictionary columns"
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
