"""
Tests for the release manager workflow registry.
"""

from __future__ import annotations

import importlib.util
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

def _load_release_workflow_registry_class():
    # Importing `...release_manager_plugins` normally executes its `__init__.py`,
    # which pulls in optional release plugins. For this unit test we only want
    # the lightweight registry type, so we load the leaf module directly.
    here = Path(__file__).resolve()
    layers_parent: Path | None = None
    for parent in [here] + list(here.parents):
        if (parent / "layers" / "__init__.py").exists():
            layers_parent = parent
            break
    assert layers_parent is not None

    registry_path = (
        layers_parent
        / "layers"
        / "layer_1_pypi"
        / "level_1_impl"
        / "level_0"
        / "plugins"
        / "release_manager_plugins"
        / "registry.py"
    )

    spec = importlib.util.spec_from_file_location("_release_manager_registry", registry_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ReleaseWorkflowRegistry


def test_release_workflow_registry_register_and_get() -> None:
    ReleaseWorkflowRegistry = _load_release_workflow_registry_class()
    reg = ReleaseWorkflowRegistry()

    def _workflow(**_kwargs):
        return "ok"

    reg.register_workflow("python_package", _workflow, {"supports_pypi": True})

    assert reg.get_workflow("python_package") is _workflow
    assert reg.get_workflow("missing") is None
    assert "python_package" in reg.list_workflows()
    assert reg.get_workflow_info("python_package") == {"supports_pypi": True}

