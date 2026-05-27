# ============================================================
# form_pipeline.py — DAG orchestrator
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    FORM_BASE_COLUMN_MAP,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    debug_form,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    reshape_form_wide_to_long,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    standardize_columns,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
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

    df = standardize_columns(df.copy(), FORM_BASE_COLUMN_MAP, strict=True)

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