# ============================================================
# merge_contracts.py — merged dataframe contract validation
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_0.schema import (
    MERGED,
)


def validate_merged_contract(
    merged: pd.DataFrame,
) -> None:
    """
    Validates required merged dataframe schema.
    """

    required = [
        MERGED.merge_flag,
    ]

    missing = [
        col
        for col in required
        if col not in merged.columns
    ]

    if missing:
        raise RuntimeError(
            f"Merge contract violation: missing columns {missing}"
        )