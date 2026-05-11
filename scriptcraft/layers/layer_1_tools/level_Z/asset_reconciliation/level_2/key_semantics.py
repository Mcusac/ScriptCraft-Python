from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_1.tag_sanitizer import (
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


def finalize_merge_key(value) -> str:
    """
    Boundary rule:
    empty → NA signal
    """

    v = normalize_merge_key_value(value)

    return v