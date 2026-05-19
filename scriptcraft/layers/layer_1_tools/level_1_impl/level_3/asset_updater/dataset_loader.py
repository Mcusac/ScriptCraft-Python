# ============================================================
# dataset_loader.py — LEVEL_3
#
# PURPOSE:
# - Load and merge reconciliation output CSVs for the updater
# ============================================================

from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import (
    log_and_print,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3.asset_updater_row_values import (
    is_present,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    constants as c,
)


def _row_has_location_change(row: Dict[str, Any]) -> bool:

    return any(
        is_present(row.get(key))
        for key in c.LOCATION_CODE_ROW_KEYS
    )


def _row_has_custodian_change(row: Dict[str, Any]) -> bool:

    return any(
        is_present(row.get(key))
        for key in c.EMPLOYEE_ID_ROW_KEYS
    )


def print_dataset_merge_summary(records: List[Dict[str, Any]]) -> None:
    """Log counts for both / location_only / custodian_only groups."""

    both = 0
    location_only = 0
    custodian_only = 0

    for row in records:

        has_location = _row_has_location_change(row)
        has_custodian = _row_has_custodian_change(row)

        if has_location and has_custodian:
            both += 1
        elif has_location:
            location_only += 1
        elif has_custodian:
            custodian_only += 1

    log_and_print(
        f"\nDataset: {len(records)} tags "
        f"(both={both}, location_only={location_only}, "
        f"custodian_only={custodian_only})"
    )


def load_updater_dataset(
    location_csv: Path,
    custodian_csv: Path,
    *,
    log_summary: bool = True,
) -> List[Dict[str, Any]]:
    """
    Union of all tags with location and/or custodian changes (outer join).
    """

    tag_dtype = {c.MERGE_ON_COLUMN: str}

    custodian_dtype = {
        c.MERGE_ON_COLUMN: str,
        "new_custodian_id": str,
        "old_custodian_id": str,
    }

    location_df = pd.read_csv(
        location_csv,
        dtype=tag_dtype,
    )

    custodian_df = pd.read_csv(
        custodian_csv,
        dtype=custodian_dtype,
    )

    merged = location_df.merge(
        custodian_df,
        on=c.MERGE_ON_COLUMN,
        how="outer",
    )

    records = merged.to_dict("records")

    if log_summary:
        print_dataset_merge_summary(records)

    return records
