from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    normalize_null,
)


def canonical_text(value) -> str:
    """
    Lossy canonical form for comparison/joining.

    Rules:
    - null → ""
    - strip
    - lowercase
    """

    s = normalize_null(value)

    if s == "":
        return ""

    return str(s).strip().lower()