# ============================================================
# detect_off_campus.py — off-campus detection
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_0.constants import (
    OFF_CAMPUS_CANONICAL,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_0.schema import (
    MERGED,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_0.predicates import (
    safe_eq,
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