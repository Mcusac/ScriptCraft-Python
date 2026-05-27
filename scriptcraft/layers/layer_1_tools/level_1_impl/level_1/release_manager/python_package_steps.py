"""
Python-package release helpers (impl-level, shared across release plugins).
"""

import os

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import get_config

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    upload_distribution_files,
)


def get_workspace_version_strategy() -> str:
    env_value = os.environ.get("WORKSPACE_VERSION_STRATEGY")
    if env_value:
        return env_value.strip().lower()

    try:
        config = get_config()
        if config is not None:
            framework_cfg = (
                config.get_framework_config()
                if hasattr(config, "get_framework_config")
                else None
            )
            packaging = getattr(framework_cfg, "packaging", None)
            if isinstance(packaging, dict):
                value = packaging.get("workspace_version_strategy")
                if isinstance(value, str) and value.strip():
                    return value.strip().lower()
    except Exception:
        pass

    return "mirror"


def upload_to_pypi(submodule_dir: Path) -> bool:
    """Upload built artifacts from a python-package submodule dist/ directory."""
    dist_dir = submodule_dir / "dist"
    return upload_distribution_files(dist_dir, cwd=submodule_dir)
