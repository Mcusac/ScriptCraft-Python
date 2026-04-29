"""
Credentials IO for `rhq_form_autofiller`.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print


def load_credentials(credentials_file: Path) -> Tuple[Optional[str], Optional[str]]:
    """
    Load credentials from a `credentials.txt` file.

    Expected format:
      username=...
      password=...
    """
    try:
        if not credentials_file.exists():
            return None, None

        credentials: Dict[str, str] = {}
        with open(credentials_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    credentials[key.strip()] = value.strip()

        username = credentials.get("username")
        password = credentials.get("password")
        if username and password:
            return username, password
        return None, None

    except Exception as e:
        log_and_print(f"⚠️ Error loading credentials: {e}", level="warning")
        return None, None

