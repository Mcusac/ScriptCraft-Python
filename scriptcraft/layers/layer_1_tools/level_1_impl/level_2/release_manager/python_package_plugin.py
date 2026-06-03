"""
Python-package release orchestration for Release Manager.

Canonical for workspace-integrated releases (submodule + workspace sync).
For standalone repo pipelines use GenericReleaseTool (level_0) + infra pipelines.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    build_submodule_package,
    bump_submodule_version,
    finalize_submodule_git,
    mirror_workspace_version_file,
    resolve_python_package_paths_or_none,
    sync_workspace_submodule_ref,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    upload_to_pypi,
)


@dataclass
class PythonPackageReleaseContext:
    submodule_dir: Path
    workspace_root: Path
    version_type: str
    auto_push: bool
    force: bool
    custom_message: Optional[str]
    skip_pypi: bool
    current_version: Optional[str] = None
    new_version: Optional[str] = None


def _validate_version_type(version_type: Optional[str]) -> bool:
    if not version_type:
        log_and_print("❌ Version type required", level="error")
        return False
    if version_type not in ("major", "minor", "patch"):
        log_and_print(f"❌ Invalid version type: {version_type}", level="error")
        return False
    return True


def _print_summary(ctx: PythonPackageReleaseContext) -> None:
    log_and_print("=" * 50)
    log_and_print(f"🎉 Released Python Package v{ctx.new_version}")
    log_and_print("\n✅ Done:")
    log_and_print(f"   • Version bump → {ctx.new_version}")
    log_and_print("   • Build complete")
    if not ctx.skip_pypi:
        log_and_print("   • PyPI upload complete")
    log_and_print("   • Git operations complete")
    log_and_print("   • Workspace synced")


def python_package_release_mode(
    input_paths: List[Path],
    output_dir: Path,
    domain: Optional[str] = None,
    version_type: Optional[str] = None,
    auto_push: bool = False,
    force: bool = False,
    custom_message: Optional[str] = None,
    skip_pypi: bool = False,
    **kwargs,
) -> None:
    _ = input_paths, output_dir, domain, kwargs
    log_and_print("🚀 Running Python Package Release Mode...")

    if not _validate_version_type(version_type):
        return

    paths = resolve_python_package_paths_or_none()
    if paths is None:
        return

    ctx = PythonPackageReleaseContext(
        submodule_dir=paths[0],
        workspace_root=paths[1],
        version_type=version_type,
        auto_push=auto_push,
        force=force,
        custom_message=custom_message,
        skip_pypi=skip_pypi,
    )

    ctx.new_version = bump_submodule_version(ctx.submodule_dir, ctx.version_type)
    if not ctx.new_version:
        return

    if not build_submodule_package(ctx.submodule_dir):
        return

    if not ctx.skip_pypi:
        if not upload_to_pypi(ctx.submodule_dir):
            log_and_print("❌ PyPI upload failed", level="error")
            return
        log_and_print("✅ PyPI upload complete")
    else:
        log_and_print("⏭️ Skipping PyPI upload")

    if not finalize_submodule_git(
        ctx.submodule_dir,
        new_version=ctx.new_version,
        version_type=ctx.version_type,
        auto_push=ctx.auto_push,
        force=ctx.force,
        custom_message=ctx.custom_message,
    ):
        return

    sync_workspace_submodule_ref(
        ctx.workspace_root,
        new_version=ctx.new_version,
        auto_push=ctx.auto_push,
    )
    mirror_workspace_version_file(
        ctx.workspace_root,
        new_version=ctx.new_version,
        auto_push=ctx.auto_push,
    )
    _print_summary(ctx)
