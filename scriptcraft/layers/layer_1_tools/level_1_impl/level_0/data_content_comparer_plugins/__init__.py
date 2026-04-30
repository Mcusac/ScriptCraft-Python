"""Mode plugin registry for the data content comparer tool (level_0).

This package owns the comparer modes and registers them into the unified registry.
"""

from __future__ import annotations

import importlib

from collections.abc import Callable
from typing import Optional

from layers.layer_1_tools.level_0_infra.level_7.registry import unified_registry

_PLUGIN_TYPE = "data_content_comparer_mode"


def _register() -> None:
    """
    Register mode plugins into the unified registry.

    This is defensive/lazy: one broken mode must not break tool imports.
    """

    modes: dict[str, tuple[str, str, dict]] = {
        "standard": (".standard_mode", "run_mode", {"description": "Standard comparison mode"}),
        "rhq": (".rhq_mode", "run_mode", {"description": "RHQ comparison mode"}),
        "domain": (".domain_old_vs_new_mode", "run_mode", {"description": "Domain old vs new comparison mode"}),
        "release_consistency": (
            ".release_consistency_mode",
            "run_mode",
            {"description": "Release consistency comparison mode"},
        ),
        "release": (
            ".release_consistency_mode",
            "run_mode",
            {"description": "Alias of release_consistency"},
        ),
    }

    for mode_name, (module_rel, func_name, meta) in modes.items():
        try:
            module = importlib.import_module(module_rel, package=__name__)
            plugin = getattr(module, func_name)
            unified_registry.register_plugin(_PLUGIN_TYPE, mode_name, plugin, meta)
        except Exception:
            # Intentionally silent: registry consumers will simply not see the mode.
            continue


_register()


def get_plugin(mode: str) -> Optional[Callable]:
    """Return the mode handler for `mode` or None if unknown."""
    return unified_registry.get_plugin(_PLUGIN_TYPE, mode)


def list_plugins() -> list[str]:
    """List available mode names."""
    listing = unified_registry.list_plugins(_PLUGIN_TYPE)
    return listing.get(_PLUGIN_TYPE, [])


__all__ = [
    "get_plugin",
    "list_plugins",
]

