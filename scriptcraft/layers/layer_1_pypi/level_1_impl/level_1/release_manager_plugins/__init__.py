"""Plugin system for Release Manager Tool.

Moved from `level_Z/release_manager/plugins/` into `level_0/release_manager_plugins/`
to support the level-based dependency architecture.

Important: keep this module import-light. Some plugins can have optional
dependencies or import-time side effects. Import plugins lazily inside
`load_builtin_plugins()` so `--help` and unit tests can still import the
registry without failing.
"""

from .registry import ReleaseWorkflowRegistry


def load_builtin_plugins(registry: ReleaseWorkflowRegistry) -> None:
    """Load all built-in plugins into the registry."""
    from .python_package_plugin import run_mode as python_package_mode
    from .workspace_plugin import run_mode as workspace_mode
    from .pypi_plugin import run_mode as pypi_mode

    # Python package release plugin
    registry.register_workflow(
        "python_package",
        python_package_mode,
        {
            "description": "Release a Python package with version bumping and PyPI upload",
            "version_types": ["major", "minor", "patch"],
            "supports_pypi": True,
            "supports_git": True,
        },
    )

    # Workspace release plugin
    registry.register_workflow(
        "workspace",
        workspace_mode,
        {
            "description": "Release a workspace with version bumping and git operations",
            "version_types": ["major", "minor", "patch"],
            "supports_pypi": False,
            "supports_git": True,
        },
    )

    # PyPI-only plugin
    registry.register_workflow(
        "pypi",
        pypi_mode,
        {
            "description": "Upload existing package to PyPI without version changes",
            "version_types": [],
            "supports_pypi": True,
            "supports_git": False,
        },
    )

    # Workspace sync plugin
    from .workspace_sync_plugin import run_mode as workspace_sync_mode

    registry.register_workflow(
        "workspace_sync",
        workspace_sync_mode,
        {
            "description": "Synchronize workspace and submodule repositories",
            "operations": ["sync", "workspace_sync", "submodule_update"],
            "supports_pypi": False,
            "supports_git": True,
        },
    )

