# ============================================================
# form_transform.py — field normalization stage
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import FORM_RAW
from scriptcraft.layers.layer_1_tools.level_1_impl.level_2 import (
    normalize_tag,
    normalize_employee_id,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_3 import (
    normalize_location,
)


def normalize_form_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df[FORM_RAW.tag] = normalize_tag(df[FORM_RAW.tag])
    df[FORM_RAW.emp_id] = normalize_employee_id(df[FORM_RAW.emp_id])
    df[FORM_RAW.location] = normalize_location(df[FORM_RAW.location])

    return df