"""
Python Package Release Plugin for Release Manager Tool.

This plugin handles releasing Python packages with version bumping, building, and PyPI uploading.
"""

import os
import shutil

from pathlib import Path
from typing import List, Optional

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_2.root_schema import get_config

from layers.layer_1_tools.level_1_impl.level_0.subprocess.runner import run_str, run_ok
from layers.layer_1_tools.level_1_impl.level_0.versioning.messages import get_commit_message
from layers.layer_1_tools.level_1_impl.level_0.versioning.semver import bump_version
from layers.layer_1_tools.level_1_impl.level_0.versioning.version_file import (
    get_current_version,
    update_version_file,
)


# ============================================================
# CONFIG / STRATEGY
# ============================================================

def _get_workspace_version_strategy() -> str:
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


# ============================================================
# BUILD UTILITIES
# ============================================================

def clean_build_artifacts(submodule_dir: Path) -> None:
    log_and_print("🧹 Cleaning build artifacts...")

    targets = [
        submodule_dir / "dist",
        submodule_dir / "build",
    ]

    for path in targets:
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
            log_and_print(f"🗑️ Removed {path.name}")

    # egg-info wildcard handling
    for egg in submodule_dir.glob("*.egg-info"):
        shutil.rmtree(egg, ignore_errors=True)
        log_and_print(f"🗑️ Removed {egg.name}")


def build_package(submodule_dir: Path) -> bool:
    return run_ok(
        "python -m build",
        "Building package",
        cwd=submodule_dir,
    )


def upload_to_pypi(submodule_dir: Path) -> bool:
    return run_ok(
        "python -m twine upload dist/*",
        "Uploading to PyPI",
        cwd=submodule_dir,
    )


# ============================================================
# MAIN RELEASE FLOW
# ============================================================

def run_mode(
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

    log_and_print("🚀 Running Python Package Release Mode...")

    # -------------------------
    # VALIDATION
    # -------------------------
    if not version_type:
        log_and_print("❌ Version type required", level="error")
        return

    if version_type not in ["major", "minor", "patch"]:
        log_and_print(f"❌ Invalid version type: {version_type}", level="error")
        return

    # -------------------------
    # RESOLVE PATHS (NO os.chdir)
    # -------------------------
    original_cwd = Path.cwd()

    if original_cwd.name == "python-package":
        submodule_dir = original_cwd
    else:
        submodule_dir = original_cwd / "implementations/python-package"

    if not submodule_dir.exists():
        log_and_print("❌ Cannot find python-package directory", level="error")
        return

    workspace_root = submodule_dir.parent.parent if submodule_dir.name == "python-package" else original_cwd

    log_and_print(f"📁 Submodule: {submodule_dir}")
    log_and_print(f"🏠 Workspace: {workspace_root}")

    # -------------------------
    # VERSION
    # -------------------------
    current_version = get_current_version()
    if not current_version:
        return

    new_version = bump_version(current_version, version_type)
    if not new_version:
        return

    log_and_print(f"🔄 {current_version} → {new_version}")

    if not update_version_file(new_version):
        return

    # -------------------------
    # BUILD + PYPI
    # -------------------------
    clean_build_artifacts(submodule_dir)

    if not build_package(submodule_dir):
        log_and_print("❌ Build failed", level="error")
        return

    if not skip_pypi:
        if not upload_to_pypi(submodule_dir):
            log_and_print("❌ PyPI upload failed", level="error")
            return
        log_and_print("✅ PyPI upload complete")
    else:
        log_and_print("⏭️ Skipping PyPI upload")

    # -------------------------
    # GIT SUBMODULE OPERATIONS
    # -------------------------
    if run_str("git status --porcelain", "Checking git status", cwd=submodule_dir) is None:
        return

    if not run_ok("git add .", "Staging changes", cwd=submodule_dir):
        return

    status = run_str("git status --porcelain", "Checking staged changes", cwd=submodule_dir)

    if not status and not force:
        log_and_print("⚠️ No changes to commit", level="warning")
        return

    commit_message = (
        custom_message
        or get_commit_message(new_version, version_type)
    )

    if not run_ok(f'git commit -m "{commit_message}"', "Committing", cwd=submodule_dir):
        return

    existing_tag = run_str(f"git tag -l v{new_version}", "Checking tag", cwd=submodule_dir)
    if not existing_tag:
        run_ok(f"git tag v{new_version}", "Creating tag", cwd=submodule_dir)

    if auto_push:
        run_ok("git push origin main", "Pushing commits", cwd=submodule_dir)
        run_ok(f"git push origin v{new_version}", "Pushing tag", cwd=submodule_dir)

    # -------------------------
    # WORKSPACE UPDATE (NO DIR CHANGE)
    # -------------------------
    log_and_print("🔄 Updating workspace reference...")

    run_ok(
        "git submodule update --remote implementations/python-package",
        "Updating submodule ref",
        cwd=workspace_root,
    )

    if run_ok(
        "git add implementations/python-package",
        "Staging submodule ref",
        cwd=workspace_root,
    ):
        run_ok(
            f'git commit -m "📦 Update python-package v{new_version}"',
            "Committing workspace update",
            cwd=workspace_root,
        )

        if auto_push:
            run_ok("git push origin main", "Pushing workspace", cwd=workspace_root)

    # -------------------------
    # STRATEGY MIRROR
    # -------------------------
    strategy = _get_workspace_version_strategy()
    log_and_print(f"🧭 Strategy: {strategy}")

    if strategy == "mirror":
        try:
            version_file = workspace_root / "VERSION"
            version_file.write_text(f"{new_version}\n", encoding="utf-8")

            if run_ok("git add VERSION", "Staging VERSION", cwd=workspace_root):

                run_ok(
                    f'git commit -m "Workspace v{new_version} (mirror)"',
                    "Committing workspace version",
                    cwd=workspace_root,
                )

                if not run_str(f"git tag -l v{new_version}", "Checking tag", cwd=workspace_root):
                    run_ok(f"git tag v{new_version}", "Tagging workspace", cwd=workspace_root)

                if auto_push:
                    run_ok("git push origin main", "Pushing workspace", cwd=workspace_root)
                    run_ok(f"git push origin v{new_version}", "Pushing tag", cwd=workspace_root)

        except Exception as e:
            log_and_print(f"⚠️ Mirror failed: {e}", level="warning")

    # -------------------------
    # SUMMARY
    # -------------------------
    log_and_print("=" * 50)
    log_and_print(f"🎉 Released Python Package v{new_version}")

    log_and_print("\n✅ Done:")
    log_and_print(f"   • {current_version} → {new_version}")
    log_and_print("   • Build complete")
    if not skip_pypi:
        log_and_print("   • PyPI upload complete")
    log_and_print("   • Git operations complete")
    log_and_print("   • Workspace synced")