# ============================================================
# credentials_loader.py — LEVEL_1
#
# PURPOSE:
# - Load optional local credentials from gitignored credentials.py
# ============================================================

from typing import Optional
from typing import Tuple


def load_credentials() -> Optional[Tuple[str, str]]:
    """
    Return (username, password) when credentials.py exists and is populated.
    """

    try:

        from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
            UNT_PASSWORD,
            UNT_USERNAME,
        )

    except ImportError:
        return None

    username = str(UNT_USERNAME).strip()
    password = str(UNT_PASSWORD).strip()

    if not username or not password:
        return None

    if username == "your_euid" or password == "your_password":
        return None

    return username, password


def load_authorizer_name() -> str | None:
    """
    Return authorized-by display name when credentials.py defines it.
    """

    try:

        from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
            AUTHORIZED_BY_NAME,
        )

    except ImportError:
        return None

    name = str(AUTHORIZED_BY_NAME).strip()

    if not name or name == "Your Full Name":
        return None

    return name
