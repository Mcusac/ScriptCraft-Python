# ============================================================
# credentials_loader.py — LEVEL_1
#
# PURPOSE:
# - Load optional local credentials from gitignored credentials.py
# ============================================================

from pathlib import Path
from typing import Dict, Optional, Tuple

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    AUTHORIZED_BY_NAME,
    UNT_PASSWORD,
    UNT_USERNAME,
    log_and_print,
)


def load_credentials(credentials_file: Path | None = None) -> Optional[Tuple[str, str]]:
    """
    Return (username, password) from either:
    - a `credentials.txt` file (when `credentials_file` is provided), or
    - credentials.py constants (default behavior).
    """
    if credentials_file is not None:
        return _load_credentials_from_file(credentials_file)

    username = str(UNT_USERNAME).strip()
    password = str(UNT_PASSWORD).strip()

    if not username or not password:
        return None

    if username == "your_euid" or password == "your_password":
        return None

    return username, password


def _load_credentials_from_file(credentials_file: Path) -> Optional[Tuple[str, str]]:
    """
    Return (username, password) from `credentials.txt` key=value lines.
    """
    try:
        if not credentials_file.exists():
            return None

        credentials: Dict[str, str] = {}
        with open(credentials_file, "r", encoding="utf-8") as credentials_stream:
            for line in credentials_stream:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    credentials[key.strip()] = value.strip()

        username = credentials.get("username")
        password = credentials.get("password")
        if username and password:
            return username, password
        return None
    except Exception as exc:
        log_and_print(
            f"⚠️ Error loading credentials from {credentials_file}: {exc}",
            level="warning",
        )
        return None


def load_authorizer_name() -> str | None:
    """
    Return authorized-by display name when credentials.py defines it.
    """

    name = str(AUTHORIZED_BY_NAME).strip()

    if not name or name == "Your Full Name":
        return None

    return name
