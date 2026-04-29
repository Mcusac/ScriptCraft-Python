"""
Shared environment helpers for tool-local env modules.

This module centralizes shared environment import helpers so env modules can
stay thin and declarative.
"""
from types import ModuleType


def import_module_dual(dev_module: str, dist_module: str) -> ModuleType:
    """
    Import a module by name with a distributable fallback.
    """
    import importlib

    try:
        return importlib.import_module(dev_module)
    except ImportError:
        try:
            return importlib.import_module(dist_module)
        except ImportError as e:
            raise ImportError(f"Could not import {dev_module!r} or {dist_module!r}: {e}") from e