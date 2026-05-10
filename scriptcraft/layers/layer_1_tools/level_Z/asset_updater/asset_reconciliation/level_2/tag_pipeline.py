import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.tag_rules import (
    apply_tag_rules,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_1.tag_sanitizer import (
    sanitize_tag,
)


def _tag_pipeline(value) -> str:
    return apply_tag_rules(sanitize_tag(value))


def _id_pipeline(value) -> str:
    return sanitize_tag(value)


def normalize_tag(series: pd.Series) -> pd.Series:
    return series.map(_tag_pipeline)


def normalize_employee_id(series: pd.Series) -> pd.Series:
    return series.map(_id_pipeline)