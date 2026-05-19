import pandas as pd

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    apply_tag_rules,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    sanitize_tag,
)


def _tag_pipeline(value) -> str:
    return apply_tag_rules(sanitize_tag(value))


def normalize_tag(series: pd.Series) -> pd.Series:
    return series.map(_tag_pipeline)


def normalize_employee_id(series: pd.Series) -> pd.Series:
    return series.map(sanitize_tag)
