"""Lazy access to dictionary-checker configuration."""

from functools import lru_cache
from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_5 import load_config


@lru_cache(maxsize=1)
def get_dictionary_checker_config() -> Dict[str, Any]:
    """Return the workspace ``dictionary_checker`` config section."""

    config = load_config()
    section = getattr(config, "dictionary_checker", None)
    if isinstance(section, dict):
        return section
    return {}


def get_plugin_config(section_key: str) -> Dict[str, Any]:
    """Return a named subsection (e.g. ``date_validation``) with a dict default."""
    section = get_dictionary_checker_config().get(section_key, {})
    return section if isinstance(section, dict) else {}
