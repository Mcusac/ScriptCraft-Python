# ============================================================
# asset_normalizer.py — asset field normalization stage
# ============================================================
import pandas as pd

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import ASSET_RAW
from scriptcraft.layers.layer_1_tools.level_1_impl.level_2 import normalize_tag, normalize_employee_id
from scriptcraft.layers.layer_1_tools.level_1_impl.level_3 import normalize_location


def normalize_asset_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df[ASSET_RAW.tag] = normalize_tag(df[ASSET_RAW.tag])
    df[ASSET_RAW.emp_id] = normalize_employee_id(df[ASSET_RAW.emp_id])
    df[ASSET_RAW.location] = normalize_location(df[ASSET_RAW.location])

    return df