# ============================================================
# detect_off_campus.py — off-campus detection
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_0_core.level_0 import safe_eq

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    OFF_CAMPUS_CANONICAL,
    MERGED,
)


def detect_off_campus(
    merged: pd.DataFrame,
) -> pd.DataFrame:
    """
    Detect assets marked off-campus
    in either asset or form datasets.
    """

    asset_off = safe_eq(
        merged,
        MERGED.asset_location,
        OFF_CAMPUS_CANONICAL,
    )

    form_off = safe_eq(
        merged,
        MERGED.form_location,
        OFF_CAMPUS_CANONICAL,
    )

    return merged.loc[
        asset_off | form_off,
        [
            MERGED.tag,
            MERGED.asset_location,
            MERGED.form_location,
            MERGED.merge_flag,
        ],
    ].copy()