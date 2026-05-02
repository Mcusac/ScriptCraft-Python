"""
Configuration loader (single source of I/O).

Responsibilities:
- load config.yaml (if present)
- fallback to env vars
- fallback to defaults

NO constants, NO path logic, NO filesystem utilities beyond config.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict

from layers.layer_1_tools.level_0_infra.level_0.environment import detect_environment

_config_cache: Dict[str, Any] | None = None


def load_config() -> Dict[str, Any]:
    """
    Lazy-load configuration once.
    """
    global _config_cache

    if _config_cache is not None:
        return _config_cache

    # 1. search for config.yaml
    search_paths = [
        Path(__file__).resolve().parents[i] / "config.yaml"
        for i in range(3, 6)
    ] + [Path.cwd() / "config.yaml"]

    for path in search_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    _config_cache = yaml.safe_load(f) or {}
                    return _config_cache
            except Exception:
                continue

    # 2. env-based production fallback
    if detect_environment() == "production":
        _config_cache = {
            "study_name": os.environ.get("STUDY_NAME", "DEFAULT_STUDY"),
            "id_columns": os.environ.get("ID_COLUMNS", "Med_ID,Visit_ID").split(","),
            "output_dir": os.environ.get("OUTPUT_DIR", "output"),
            "log_level": os.environ.get("LOG_LEVEL", "INFO"),
            "domains": os.environ.get("DOMAINS", "").split(",") if os.environ.get("DOMAINS") else [],
            "folder_structure": {},
        }
        return _config_cache

    # 3. dev defaults
    _config_cache = {
        "study_name": "DEFAULT_STUDY",
        "id_columns": ["Med_ID", "Visit_ID"],
        "output_dir": "output",
        "log_level": "INFO",
        "domains": [],
        "folder_structure": {},
    }

    return _config_cache


def get_config(key: str | None = None, default: Any = None) -> Any:
    cfg = load_config()
    return cfg if key is None else cfg.get(key, default)