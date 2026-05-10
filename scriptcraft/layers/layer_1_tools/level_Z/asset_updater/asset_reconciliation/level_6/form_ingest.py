# ============================================================
# form_ingest.py — form normalization layer
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_5.form_pipeline import (
    normalize_form,
)


def ingest_forms(form_df_raw: pd.DataFrame) -> pd.DataFrame:
    return normalize_form(form_df_raw)