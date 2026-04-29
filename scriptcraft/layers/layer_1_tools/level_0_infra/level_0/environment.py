"""
Environment detection: distinguishes development from distributable (production) mode.
"""

import os
from pathlib import Path


def detect_environment() -> str:
    """
    Return 'development' or 'production' based on runtime indicators.

    Checks, in order:
    1. SCRIPTCRAFT_ENV environment variable (explicit override).
    2. Presence of config.yaml + implementations/ (development workspace).
    3. Any distributable-mode marker (embedded Python, batch scripts, env vars, naming).
    """
    explicit = os.environ.get("SCRIPTCRAFT_ENV")
    if explicit:
        return explicit

    cwd = Path(".")

    if (cwd / "config.yaml").exists() and (cwd / "implementations").exists():
        return "development"

    distributable_indicators = (
        (cwd / "embed_py311").exists(),
        (cwd / "config.bat").exists(),
        (cwd / "run.bat").exists(),
        os.environ.get("TOOL_TO_SHIP") is not None,
        cwd.name.endswith("_distributable"),
    )

    if any(distributable_indicators):
        return "production"

    # Default: assume development when no distributable markers are present.
    return "development"