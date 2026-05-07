import pandas as pd
from schema import ASSET_RAW
from tag_normalizer import normalize_tag, normalize_employee_id
from location_normalizer import normalize_location


def normalize_asset_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df[ASSET_RAW.tag] = normalize_tag(df[ASSET_RAW.tag])
    df[ASSET_RAW.emp_id] = normalize_employee_id(df[ASSET_RAW.emp_id])
    df[ASSET_RAW.location] = normalize_location(df[ASSET_RAW.location])

    return df