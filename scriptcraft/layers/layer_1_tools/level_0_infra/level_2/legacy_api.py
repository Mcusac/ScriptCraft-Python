"""
Legacy compatibility layer.

Keeps old imports working while system migrates to clean architecture.
"""

from layers.layer_1_tools.level_0_infra.level_1.config_loader import get_config


def get_legacy_config(key=None, default=None):
    cfg = get_config()
    return cfg if key is None else cfg.get(key, default)