"""Tests for builtin release_manager plugin registration."""

from __future__ import annotations

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    ReleaseWorkflowRegistry,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_3 import (
    load_builtin_plugins,
)


def test_load_builtin_plugins_registers_expected_modes() -> None:
    registry = ReleaseWorkflowRegistry()
    load_builtin_plugins(registry)
    modes = set(registry.list_workflows())
    assert modes >= {
        "pypi",
        "python_package",
        "workspace",
        "workspace_sync",
        "sync",
    }
    for mode in ("pypi", "python_package", "workspace"):
        assert registry.get_workflow(mode) is not None
        info = registry.get_workflow_info(mode)
        assert info is not None
        assert "description" in info
