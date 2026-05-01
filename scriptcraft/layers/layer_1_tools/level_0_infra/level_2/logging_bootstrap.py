import yaml
import logging

from pathlib import Path
from typing import Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_primitives import LogConfig
from layers.layer_1_tools.level_0_infra.level_1.paths import get_project_root, LOG_LEVEL


def _load_verbose_mode(config_file: Path, default: bool) -> Optional[bool]:
    if not config_file.exists():
        return None

    try:
        with open(config_file, encoding="utf-8", errors="replace") as f:
            data = yaml.safe_load(f) or {}
        return data.get("verbose_mode", default)
    except Exception as e:
        logging.warning(f"Failed to load verbose mode from {config_file}: {e}")
        return None


def build_log_config() -> LogConfig:
    """
    Central bootstrap for LogConfig (keeps precedence logic intact)
    """

    config = LogConfig(
        log_level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        default_log_dir="logs",
    )

    local_config = Path("config.yaml")
    project_config = get_project_root() / "config.yaml"

    # local override
    local_value = _load_verbose_mode(local_config, True)
    if local_value is not None:
        config.set_verbose_mode(local_value)
    else:
        config.set_verbose_mode(True)

    # project override
    project_value = _load_verbose_mode(project_config, False)
    if project_value is not None:
        config.set_verbose_mode(project_value)
    else:
        config.set_verbose_mode(False)

    return config