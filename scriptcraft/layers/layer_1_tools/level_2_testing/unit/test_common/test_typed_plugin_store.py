"""
Tests for typed plugin store helpers.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _prepend_layers_parent_to_syspath() -> None:
    here = Path(__file__).resolve()
    for parent in [here] + list(here.parents):
        if (parent / "layers" / "__init__.py").exists():
            sys.path.insert(0, str(parent))
            return
    raise RuntimeError("Could not locate `layers/__init__.py` for test imports.")


_prepend_layers_parent_to_syspath()

from layers.layer_1_pypi.level_0_infra.level_0.typed_plugin_store import get_typed_plugin  # noqa: E402


def test_get_typed_plugin_returns_match() -> None:
    plugins = {
        "validator": {
            "v1": object(),
        },
        "tool": {
            "t1": object(),
        },
    }
    assert get_typed_plugin(plugins, "validator", "v1") is plugins["validator"]["v1"]


def test_get_typed_plugin_returns_none_when_missing() -> None:
    plugins = {"validator": {"v1": object()}}
    assert get_typed_plugin(plugins, "validator", "missing") is None
    assert get_typed_plugin(plugins, "missing_type", "v1") is None

