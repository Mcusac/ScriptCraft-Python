"""Tests for layer_1 PluginRegistry lookup behavior."""

from __future__ import annotations

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1.plugin_registry import (
    PluginBase,
    PluginRegistry,
)


class _StubValidator(PluginBase):
    def get_plugin_type(self) -> str:
        return "validator"


def test_plugin_registry_get_plugin_returns_registered_class() -> None:
    registry = PluginRegistry()
    registry.register_plugin("validator", "date", _StubValidator)

    assert registry.get_plugin("validator", "date") is _StubValidator


def test_plugin_registry_get_plugin_returns_none_when_missing() -> None:
    registry = PluginRegistry()

    assert registry.get_plugin("validator", "missing") is None
    assert registry.get_plugin("missing_type", "date") is None


def test_plugin_registry_list_plugins_by_type() -> None:
    registry = PluginRegistry()
    registry.register_plugin("validator", "date", _StubValidator)
    registry.register_plugin("validator", "pattern", _StubValidator)

    assert registry.list_plugins("validator") == ["date", "pattern"]
