<<<<<<< HEAD
=======
import pandas as pd
>>>>>>> 182d6be043d82fdc23c5fc4c567ad4e195b94c00
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_0.null_semantics import (
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