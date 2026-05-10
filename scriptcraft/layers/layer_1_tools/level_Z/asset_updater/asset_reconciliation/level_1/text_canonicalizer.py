from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.null_semantics import (
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