"""Import helpers for dual dev/dist module resolution."""

import importlib

from types import ModuleType


def import_module_dual(dev_module: str, dist_module: str) -> ModuleType:
    """Import dev module first, then fallback to dist module."""
    try:
        return importlib.import_module(dev_module)
    except ImportError:
        try:
            return importlib.import_module(dist_module)
        except ImportError as e:
            raise ImportError(f"Could not import {dev_module!r} or {dist_module!r}: {e}") from e
