import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    TagNormalizationMode,
    sanitize_scalar_tag,
    apply_tag_rules,
)


def _sanitize_tag(value) -> str:
    return sanitize_scalar_tag(
        value,
        mode=TagNormalizationMode.RECONCILIATION_STRUCTURAL,
    )


def _tag_pipeline(value) -> str:
    return apply_tag_rules(_sanitize_tag(value))


def normalize_tag(series: pd.Series) -> pd.Series:
    return series.map(_tag_pipeline)


def normalize_employee_id(series: pd.Series) -> pd.Series:
    return series.map(_sanitize_tag)
