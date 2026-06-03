"""PyPI upload helpers for python-package submodule releases."""

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    get_workspace_version_strategy,
    upload_distribution_files,
)


def upload_to_pypi(submodule_dir: Path) -> bool:
    """Upload built artifacts from a python-package submodule dist/ directory."""
    return upload_distribution_files(submodule_dir / "dist", cwd=submodule_dir)
