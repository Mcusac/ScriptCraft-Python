import os

from pathlib import Path


def detect_environment() -> str:
    if os.environ.get("SCRIPTCRAFT_ENV"):
        return os.environ["SCRIPTCRAFT_ENV"]

    if Path("config.yaml").exists() and Path("implementations").exists():
        return "development"

    current_dir = Path(".")
    distributable_indicators = [
        (current_dir / "embed_py311").exists(),
        (current_dir / "config.bat").exists(),
        (current_dir / "run.bat").exists(),
        os.environ.get("TOOL_TO_SHIP") is not None,
        current_dir.name.endswith("_distributable"),
    ]

    if any(distributable_indicators):
        return "production"

    return "development"