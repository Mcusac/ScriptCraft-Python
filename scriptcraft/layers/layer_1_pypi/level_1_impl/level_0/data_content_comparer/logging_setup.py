"""Logging setup for the data content comparer tool."""

from pathlib import Path
from typing import Optional

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_pypi.level_0_infra.level_3.logging_utils import setup_logging_with_timestamp


def setup_file_logging(*, log_dir: Optional[Path]) -> None:
    if not log_dir:
        return

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = setup_logging_with_timestamp(log_dir, mode="data_content_comparer")
        log_and_print(f"📝 Logging to: {log_file}")
    except Exception as e:
        log_and_print(f"⚠️ Could not set up file logging: {e}", level="warning")


def resolve_log_dir(config) -> Path:
    """
    Resolve log directory from config with safe fallbacks.

    `config` is expected to be ScriptCraft's runtime config object (attribute-based).
    """

    default_dir = Path("data/logs")
    if not config:
        return default_dir

    try:
        workspace_config = config.get_workspace_config()
        if workspace_config and hasattr(workspace_config, "logging"):
            log_config = workspace_config.logging
            if isinstance(log_config, dict) and "log_dir" in log_config:
                return Path(log_config["log_dir"])
    except Exception:
        return default_dir

    return default_dir

