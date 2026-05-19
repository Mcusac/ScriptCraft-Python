from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    normalize_null,
)


def sanitize_tag(value) -> str:
    """
    Structural cleanup only.

    NO business rules allowed.
    """

    s = normalize_null(value)

    if s == "":
        return ""

    s = str(s).strip()

    if s.endswith(".0"):
        s = s[:-2]

    return s.replace(" ", "")