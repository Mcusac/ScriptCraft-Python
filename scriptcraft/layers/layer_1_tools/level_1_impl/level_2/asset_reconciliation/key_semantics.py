from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    sanitize_tag,
)


def normalize_merge_key_value(value) -> str:
    """
    Scalar-safe merge key normalization.

    NO pandas logic here.
    """

    v = sanitize_tag(value)

    if not v:
        return ""

    return v
