"""Reusable comparison workflow executors for tool modes."""
import pandas as pd

from pathlib import Path
from typing import Any, Callable, List, Optional, Sequence, Union

from scriptcraft.layers.layer_0_core.level_0 import PipelineResult

from scriptcraft.layers.layer_0_core.level_1 import normalize_value
from scriptcraft.layers.layer_0_core.level_5 import load_comparison_pair

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    get_column_letter,
    get_domain_paths,
    get_project_root,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import compare_dataframes

PathLike = Union[str, Path]


def _ensure_output_dir(output_dir: PathLike) -> Path:
  path = Path(output_dir)
  path.mkdir(parents=True, exist_ok=True)
  return path


def run_pairwise_comparison(
  *,
  mode: str,
  input_paths: Sequence[PathLike],
  output_dir: PathLike,
  domain: Optional[str] = None,
  required_count: int = 2,
) -> PipelineResult:
  """Standard two-file comparison using compare_dataframes."""
  if not input_paths or len(input_paths) != required_count:
    raise ValueError(f"{mode} mode requires exactly {required_count} input files.")

  suffix = f" for domain: {domain}" if domain else ""
  log_and_print(f"Running {mode} comparison{suffix}...")

  try:
    df1, df2, dataset_name = load_comparison_pair(list(input_paths))
    out = _ensure_output_dir(output_dir)
    compare_dataframes(df1, df2, dataset_name, out)
    log_and_print(f"Results saved to: {out.resolve()}")
    return PipelineResult.ok(
      stage=str(mode),
      artifacts={"output_dir": str(out)},
      metadata={"dataset": dataset_name, "outputs": []},
    )
  except Exception as exc:
    log_and_print(f"{mode} comparison failed: {exc}")
    return PipelineResult.fail(stage=str(mode), error=str(exc))


def run_domain_discovery_comparison(
  *,
  mode: str,
  output_dir: PathLike,
  old_glob: str = "*.xlsx",
  new_glob: str = "*.xlsx",
) -> PipelineResult:
  """Compare latest old/new files per configured domain."""
  log_and_print(f"Running {mode} domain comparison...")
  out = _ensure_output_dir(output_dir)
  processed: List[str] = []
  failures: List[str] = []

  try:
    project_root = get_project_root()
    domain_paths = get_domain_paths(project_root)

    for domain_name, paths in domain_paths.items():
      log_and_print(f"Comparing domain: {domain_name}")
      try:
        old_candidates = list(paths["old_data"].glob(old_glob))
        new_candidates = list(paths["processed_data"].glob(new_glob))
        if not old_candidates or not new_candidates:
          raise FileNotFoundError(f"No files found for domain {domain_name}")

        old_file = sorted(old_candidates)[-1]
        new_file = sorted(new_candidates)[-1]
        df1, df2, dataset_name = load_comparison_pair([old_file, new_file])
        compare_dataframes(df1, df2, dataset_name, out)
        processed.append(domain_name)
      except Exception as exc:
        log_and_print(f"Failed comparison for {domain_name}: {exc}")
        failures.append(f"{domain_name}: {exc}")

    if failures:
      return PipelineResult.fail(
        stage=str(mode),
        error="One or more domains failed comparison",
        artifacts={"output_dir": str(out)},
        metadata={"processed_domains": processed, "failed_domains": failures, "outputs": []},
      )
    return PipelineResult.ok(
      stage=str(mode),
      artifacts={"output_dir": str(out)},
      metadata={"processed_domains": processed, "failed_domains": failures, "outputs": []},
    )
  except Exception as exc:
    return PipelineResult.fail(stage=str(mode), error=str(exc))


def run_keyed_cell_comparison(
  *,
  mode: str,
  input_paths: Sequence[PathLike],
  output_dir: PathLike,
  keys: Sequence[str],
  domain: Optional[str] = None,
  value_normalizer: Callable[[Any], Any] = normalize_value,
) -> PipelineResult:
  """Outer-merge on keys and emit per-cell discrepancy report."""
  if not input_paths or len(input_paths) != 2:
    raise ValueError(f"{mode} mode requires exactly two input files.")

  suffix = f" for domain: {domain}" if domain else ""
  log_and_print(f"Running {mode} keyed comparison{suffix}...")

  try:
    df1, df2, dataset_name = load_comparison_pair(list(input_paths))
    missing_keys = [k for k in keys if k not in df1.columns or k not in df2.columns]
    if missing_keys:
      raise ValueError(f"Missing required columns: {missing_keys}")

    merged = pd.merge(
      df1,
      df2,
      on=list(keys),
      how="outer",
      suffixes=("_A1", "_A2"),
      indicator=True,
    )

    discrepancies: List[dict[str, Any]] = []
    column_positions = {col: idx + 1 for idx, col in enumerate(df1.columns)}

    for idx, row in merged.iterrows():
      for col in df1.columns:
        if col in keys:
          continue
        val1 = row.get(f"{col}_A1", pd.NA)
        val2 = row.get(f"{col}_A2", pd.NA)
        norm_val1 = value_normalizer(val1)
        norm_val2 = value_normalizer(val2)
        if norm_val1 != norm_val2:
          col_letter = get_column_letter(column_positions[col])
          discrepancies.append(
            {
              "Med_ID": row.get(keys[0]) if keys else None,
              "Column": col,
              "Cell": f"{col_letter}{idx + 2}",
              "Assistant1": norm_val1,
              "Assistant2": norm_val2,
            }
          )

    out = _ensure_output_dir(output_dir)
    discrepancy_file = out / f"{dataset_name}_discrepancy_list.xlsx"
    pd.DataFrame(discrepancies).to_excel(discrepancy_file, index=False)
    upload_ready_file = out / f"{dataset_name}_upload_ready.xlsx"
    df1.to_excel(upload_ready_file, index=False)

    log_and_print(f"Discrepancy report saved to: {discrepancy_file.resolve()}")
    outputs = [discrepancy_file, upload_ready_file]
    return PipelineResult.ok(
      stage=str(mode),
      artifacts={
        "discrepancy_file": str(discrepancy_file),
        "upload_ready_file": str(upload_ready_file),
      },
      metadata={"dataset": dataset_name, "outputs": [str(p) for p in outputs], "discrepancies": len(discrepancies)},
    )
  except Exception as exc:
    log_and_print(f"{mode} keyed comparison failed: {exc}")
    return PipelineResult.fail(stage=str(mode), error=str(exc))
