from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    TagNormalizationMode,
    sanitize_scalar_tag,
)


def normalize_merge_key_value(value) -> str:
    """
    Scalar-safe merge key normalization.

    NO pandas logic here.
    """

    v = sanitize_scalar_tag(
        value,
        mode=TagNormalizationMode.RECONCILIATION_STRUCTURAL,
    )

    if not v:
        return ""

    return v
