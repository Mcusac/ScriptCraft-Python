from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    normalize_null_reconciliation,
)


def canonical_text(value) -> str:
    """
    Lossy canonical form for comparison/joining.

    Rules:
    - null → ""
    - strip
    - lowercase
    """

    s = normalize_null_reconciliation(value)

    if s == "":
        return ""

    return str(s).strip().lower()
