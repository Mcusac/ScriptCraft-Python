# ============================================================
# form_transform.py — field normalization stage
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.schema import FORM_RAW
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_2.tag_pipeline import (
    normalize_tag,
    normalize_employee_id,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_3.location_normalizer import (
    normalize_location,
)


def normalize_form_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df[FORM_RAW.tag] = normalize_tag(df[FORM_RAW.tag])
    df[FORM_RAW.emp_id] = normalize_employee_id(df[FORM_RAW.emp_id])
    df[FORM_RAW.location] = normalize_location(df[FORM_RAW.location])

    return df