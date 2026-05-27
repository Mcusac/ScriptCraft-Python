# ============================================================
# form_reshape.py — wide → long transformation
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import FORM_RAW
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    build_full_name,
    extract_device_columns,
    safe_get,
)


def reshape_form_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    records = []

    tag_cols, _ = extract_device_columns(df)

    for _, row in df.iterrows():

        employee_name = build_full_name(row)
        emp_id = safe_get(row, FORM_RAW.emp_id)

        for tag_col in tag_cols:

            idx = tag_col.replace("Device Tag", "")

            if idx == "":
                loc_col = "Location of Device (ie HP 505 or Off Campus)"
            else:
                loc_col = f"Location of Device (ie HP 505 or Off Campus){idx}"

            tag = safe_get(row, tag_col)
            location = safe_get(row, loc_col)

            if pd.isna(tag) or str(tag).strip() == "":
                continue

            records.append({
                FORM_RAW.tag: str(tag).strip(),
                FORM_RAW.emp_id: emp_id,
                FORM_RAW.location: location,
                "employee_name": employee_name,
            })

    return pd.DataFrame(records)