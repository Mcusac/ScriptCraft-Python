# ============================================================
# asset_pipeline.py — asset normalization pipeline
# ============================================================
import pandas as pd

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    ASSET_COLUMN_MAP,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    standardize_columns,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    ASSET_RAW,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    filter_computers_only,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_4 import (
    normalize_asset_fields,
)


# ------------------------------------------------------------
# FINAL PIPELINE (ORCHESTRATION ONLY)
# ------------------------------------------------------------

def clean_asset_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Asset normalization pipeline (DAG-safe):

        1. Standardize schema
        2. Filter domain records
        3. Normalize fields
        4. Clean custodians
    """

    df = df.copy()

    # STEP 1 — schema alignment
    df = standardize_columns(
        df,
        ASSET_COLUMN_MAP,
    )

    # STEP 2 — domain filtering (pure stage)
    df = filter_computers_only(df)

    # STEP 3 — field normalization (pure reusable pipeline)
    df = normalize_asset_fields(df)

    # STEP 4 — custodian cleanup
    cust = ASSET_RAW.custodian

    if cust in df.columns:
        df[cust] = (
            df[cust]
            .astype("string")
            .str.strip()
        )

    return df