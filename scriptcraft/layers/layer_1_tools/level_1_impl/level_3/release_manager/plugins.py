"""Builtin release workflow registration for ReleaseManager."""

from typing import Any

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    workspace_sync_mode,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    pypi_upload_mode,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_2 import (
    python_package_release_mode,
    workspace_release_mode,
)

def load_builtin_plugins(registry: Any) -> None:
    """Register stable release workflows on the given registry."""
    builtins = {
        "pypi": (pypi_upload_mode, {"description": "Upload existing dist/ to PyPI"}),
        "python_package": (
            python_package_release_mode,
            {"description": "Python package version bump, build, and release"},
        ),
        "workspace": (
            workspace_release_mode,
            {"description": "Workspace VERSION bump and changelog release"},
        ),
        "workspace_sync": (
            workspace_sync_mode,
            {"description": "Sync python-package submodule with workspace"},
        ),
        "sync": (
            workspace_sync_mode,
            {"description": "Alias for workspace_sync"},
        ),
    }

    for mode, (workflow, info) in builtins.items():
        registry.register_workflow(mode, workflow, info)
        log_and_print(f"Registered release workflow: {mode}")
