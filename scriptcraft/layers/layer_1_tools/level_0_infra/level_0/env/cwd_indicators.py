"""CWD markers for distributable vs development tool layouts."""

import os
from pathlib import Path


def cwd_indicators_basic(tool_dir_name: str) -> dict[str, object]:
    cwd = Path.cwd()
    return {
        "tool_dir_name": tool_dir_name,
        "has_embed_py311": (cwd / "embed_py311").exists(),
        "has_config_bat": (cwd / "config.bat").exists(),
        "has_run_bat": (cwd / "run.bat").exists(),
        "has_tool_to_ship": os.environ.get("TOOL_TO_SHIP") is not None,
        "cwd_name_ends_distributable": cwd.name.endswith("_distributable"),
    }


def is_distributable_from_cwd(indicators: dict[str, object]) -> bool:
    return any(
        (
            indicators.get("has_embed_py311"),
            indicators.get("has_config_bat"),
            indicators.get("has_run_bat"),
            indicators.get("has_tool_to_ship"),
            indicators.get("cwd_name_ends_distributable"),
        ),
    )
