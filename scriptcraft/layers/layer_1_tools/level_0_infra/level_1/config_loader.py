"""
Configuration loader (dict surface for legacy callers).

Canonical typed config: level_5.config.load_config -> Config.
"""

import os
import yaml

from pathlib import Path
from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import detect_environment

_config_cache: Dict[str, Any] | None = None


def load_config_dict() -> Dict[str, Any]:
    """Lazy-load configuration once as a plain dict (legacy API)."""
    global _config_cache

    if _config_cache is not None:
        return _config_cache

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

    _config_cache = {
        "study_name": "DEFAULT_STUDY",
        "id_columns": ["Med_ID", "Visit_ID"],
        "output_dir": "output",
        "log_level": "INFO",
        "domains": [],
        "folder_structure": {},
    }

    return _config_cache


def load_config() -> Dict[str, Any]:
    """Backward-compatible alias for load_config_dict."""
    return load_config_dict()


def get_config(key: str | None = None, default: Any = None) -> Any:
    cfg = load_config_dict()
    return cfg if key is None else cfg.get(key, default)
