# ============================================================
# form_pipeline.py — DAG orchestrator
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.mappings import (
    FORM_BASE_COLUMN_MAP,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.column_standardizer import (
    standardize_columns,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.form_debug import (
    debug_form,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_2.form_reshape import (
    reshape_form_wide_to_long,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_4.form_transform import (
    normalize_form_fields,
)


def normalize_form(df: pd.DataFrame, *, debug: bool = False) -> pd.DataFrame:
    """
    DAG:

        raw
         ↓
        standardize
         ↓
        reshape
         ↓
        normalize
    """

    df = standardize_columns(df.copy(), FORM_BASE_COLUMN_MAP)

    df = reshape_form_wide_to_long(df)

    if df.empty:
        return df

    df = normalize_form_fields(df)

    # --------------------------------------------------------
    # DEBUG HOOK (optional observer)
    # --------------------------------------------------------
    if debug:
        debug_form(df)

    return df