"""Plugin initialization/config wiring for dictionary-driven validators."""

from typing import Any

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1.plugin_registry import plugin_registry

__all__ = ["initialize_plugins"]


def initialize_plugins(config: Any) -> None:
    """
    Apply config-provided settings onto registered validator plugins.

    The config object is not guaranteed to be dict-like; we only rely on attribute access.
    """

    plugin_settings = getattr(config, "plugins", {}) if hasattr(config, "plugins") else {}

    validator_plugins = plugin_registry.get_all_plugins("validator").get("validator", {})
    if not isinstance(plugin_settings, dict) or not validator_plugins:
        return

    for plugin_type, settings in plugin_settings.items():
        plugin_class = validator_plugins.get(plugin_type)
        if not plugin_class or not isinstance(settings, dict):
            continue

        for key, value in settings.items():
            setattr(plugin_class, key, value)
