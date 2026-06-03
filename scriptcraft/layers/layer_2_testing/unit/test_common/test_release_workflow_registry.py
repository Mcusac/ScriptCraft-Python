"""Tests for ReleaseWorkflowRegistry (level_0 release_manager)."""

from __future__ import annotations

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    ReleaseWorkflowRegistry,
)


def test_register_and_get_workflow() -> None:
    registry = ReleaseWorkflowRegistry()

    def _dummy_workflow(**kwargs):
        _ = kwargs

    registry.register_workflow("test_mode", _dummy_workflow, {"description": "test"})
    assert registry.has_workflow("test_mode")
    assert registry.get_workflow("test_mode") is _dummy_workflow
    assert "test_mode" in registry.list_workflows()


def test_unregister_workflow() -> None:
    registry = ReleaseWorkflowRegistry()

    def _dummy(**kwargs):
        _ = kwargs

    registry.register_workflow("temp", _dummy)
    assert registry.unregister_workflow("temp")
    assert not registry.has_workflow("temp")
