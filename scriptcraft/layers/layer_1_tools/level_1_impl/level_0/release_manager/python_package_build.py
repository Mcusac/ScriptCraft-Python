"""Python-package build and version bump steps (shared L0 mechanics)."""

from pathlib import Path
from typing import Optional, Tuple

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    log_and_print,
    resolve_python_package_paths,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    build_python_package,
    bump_version,
    clean_python_build_artifacts,
    get_current_version,
    update_version_file,
)


def resolve_python_package_paths_or_none() -> Optional[Tuple[Path, Path]]:
    submodule_dir, workspace_root = resolve_python_package_paths()
    if not submodule_dir.exists():
        log_and_print("❌ Cannot find python-package directory", level="error")
        return None
    log_and_print(f"📁 Submodule: {submodule_dir}")
    log_and_print(f"🏠 Workspace: {workspace_root}")
    return submodule_dir, workspace_root


def bump_submodule_version(submodule_dir: Path, version_type: str) -> Optional[str]:
    current = get_current_version()
    if not current:
        return None
    new_version = bump_version(current, version_type)
    if not new_version:
        return None
    log_and_print(f"🔄 {current} → {new_version}")
    if not update_version_file(new_version):
        return None
    return new_version


def build_submodule_package(submodule_dir: Path) -> bool:
    clean_python_build_artifacts(submodule_dir)
    if build_python_package(submodule_dir, clean=False):
        return True
    log_and_print("❌ Build failed", level="error")
    return False
