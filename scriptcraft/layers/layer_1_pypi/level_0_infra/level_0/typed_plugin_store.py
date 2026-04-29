"""Low-level helpers for typed plugin stores.

A typed plugin store is a nested mapping shaped like:

    plugins[plugin_type][name] -> plugin_impl

This module lives at `level_0` so higher infra levels can share the same
lookup behavior without introducing cross-level import violations.
"""

from __future__ import annotations

from typing import Mapping, Optional, TypeVar

_T = TypeVar("_T")


def get_typed_plugin(
    plugins: Mapping[str, Mapping[str, _T]],
    plugin_type: str,
    name: str,
) -> Optional[_T]:
    """Return the plugin implementation for `(plugin_type, name)` or `None`."""
    return plugins.get(plugin_type, {}).get(name)

