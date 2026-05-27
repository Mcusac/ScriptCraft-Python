import pandas as pd

from pathlib import Path
from typing import Dict

from scriptcraft.layers.layer_0_core.level_5 import load_tabular

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import standardize_columns
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import compare_dataframes
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import ArgumentValidator


def run_medvisit_integrity_check(
  *,
  domain: str,
  filenames: Dict[str, str],
  output_path: Path,
) -> None:
  log_and_print(f"🔍 Validating Med/Visit ID integrity for {domain}...")

  data_dir = Path(domain)
  df_old = load_tabular(data_dir / filenames["old"])
  df_new = load_tabular(data_dir / filenames["new"])

  df_new = standardize_columns(
    df_new,
    {"Visit": "Visit_ID", "Med ID": "Med_ID"},
  )

  comparison_result = compare_dataframes(
    df_old,
    df_new,
    dataset_name=domain,
    steps=["med_ids"],
  )

  missing_in_new, missing_in_old = comparison_result.missing_ids or (
    pd.DataFrame(),
    pd.DataFrame(),
  )

  ArgumentValidator.ensure_output_dir(output_path.parent)

  with pd.ExcelWriter(output_path) as writer:
    missing_in_new.to_excel(writer, sheet_name="Missing in New", index=False)
    missing_in_old.to_excel(writer, sheet_name="Missing in Old", index=False)

  log_and_print(f"🔍 Combos missing in new dataset: {len(missing_in_new)}")
  log_and_print(f"🔍 Combos missing in old dataset: {len(missing_in_old)}")
  log_and_print(f"✅ Comparison saved to: {output_path}")

