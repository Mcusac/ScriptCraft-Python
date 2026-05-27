"""
Python Package Release Plugin for Release Manager Tool.

Version bump, build, PyPI upload, git operations, and workspace sync.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from scriptcraft.layers.layer_0_core.level_1 import run_command

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
  resolve_python_package_paths,
  get_commit_message, 
  log_and_print
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
  build_python_package,
  clean_python_build_artifacts,
  bump_version,
  get_current_version,
  update_version_file,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
  commit_if_needed,
  ensure_tag,
  git_status_porcelain,
  push_main_and_tag,
  stage_path,
  submodule_update_remote,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
  get_workspace_version_strategy,
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


def _resolve_paths() -> Optional[Tuple[Path, Path]]:
  submodule_dir, workspace_root = resolve_python_package_paths()
  if not submodule_dir.exists():
    log_and_print("❌ Cannot find python-package directory", level="error")
    return None
  log_and_print(f"📁 Submodule: {submodule_dir}")
  log_and_print(f"🏠 Workspace: {workspace_root}")
  return submodule_dir, workspace_root


def _bump_package_version(ctx: PythonPackageReleaseContext) -> bool:
  ctx.current_version = get_current_version()
  if not ctx.current_version:
    return False
  ctx.new_version = bump_version(ctx.current_version, ctx.version_type)
  if not ctx.new_version:
    return False
  log_and_print(f"🔄 {ctx.current_version} → {ctx.new_version}")
  return update_version_file(ctx.new_version)


def _build_and_publish(ctx: PythonPackageReleaseContext) -> bool:
  clean_python_build_artifacts(ctx.submodule_dir)
  if not build_python_package(ctx.submodule_dir, clean=False):
    log_and_print("❌ Build failed", level="error")
    return False
  if ctx.skip_pypi:
    log_and_print("⏭️ Skipping PyPI upload")
    return True
  if not upload_to_pypi(ctx.submodule_dir):
    log_and_print("❌ PyPI upload failed", level="error")
    return False
  log_and_print("✅ PyPI upload complete")
  return True


def _finalize_submodule_git(ctx: PythonPackageReleaseContext) -> bool:
  sub = ctx.submodule_dir
  if git_status_porcelain(sub, "Checking git status") is None:
    return False

  commit_message = ctx.custom_message or get_commit_message(
    ctx.new_version,
    ctx.version_type,
  )
  if not commit_if_needed(
    sub,
    commit_message,
    force=ctx.force,
    status_label="Checking staged changes",
  ):
    return False

  ensure_tag(sub, ctx.new_version)
  if ctx.auto_push:
    push_main_and_tag(sub, ctx.new_version)
  return True


def _sync_workspace_reference(ctx: PythonPackageReleaseContext) -> bool:
  log_and_print("🔄 Updating workspace reference...")
  root = ctx.workspace_root
  submodule_update_remote(root)

  if stage_path(root, "implementations/python-package", "Staging submodule ref"):
    result = run_command(
      ["git", "commit", "-m", f"📦 Update python-package v{ctx.new_version}"],
      check=False,
      cwd=root,
    )
    if int(result["returncode"]) != 0:
      log_and_print("❌ Committing workspace update - FAILED", level="error")
      stderr = (result.get("stderr") or "").strip()
      if stderr:
        log_and_print(f"Error: {stderr}", level="error")
      return False
    log_and_print("✅ Committing workspace update - SUCCESS")
    if ctx.auto_push:
      push_r = run_command(["git", "push", "origin", "main"], check=False, cwd=root)
      if int(push_r["returncode"]) != 0:
        log_and_print("❌ Pushing workspace - FAILED", level="error")
        stderr = (push_r.get("stderr") or "").strip()
        if stderr:
          log_and_print(f"Error: {stderr}", level="error")
        return False
      log_and_print("✅ Pushing workspace - SUCCESS")
  return True


def _mirror_workspace_version(ctx: PythonPackageReleaseContext) -> None:
  strategy = get_workspace_version_strategy()
  log_and_print(f"🧭 Strategy: {strategy}")
  if strategy != "mirror":
    return

  root = ctx.workspace_root
  try:
    version_file = root / "VERSION"
    version_file.write_text(f"{ctx.new_version}\n", encoding="utf-8")
    add_r = run_command(["git", "add", "VERSION"], check=False, cwd=root)
    if int(add_r["returncode"]) == 0:
      commit_r = run_command(
        ["git", "commit", "-m", f"Workspace v{ctx.new_version} (mirror)"],
        check=False,
        cwd=root,
      )
      if int(commit_r["returncode"]) != 0:
        log_and_print("❌ Committing workspace version - FAILED", level="error")
      tag_r = run_command(["git", "tag", "-l", f"v{ctx.new_version}"], check=False, cwd=root)
      if not (tag_r.get("stdout") or "").strip():
        ensure_tag(root, ctx.new_version)
      if ctx.auto_push:
        push_main_and_tag(root, ctx.new_version)
  except Exception as e:
    log_and_print(f"⚠️ Mirror failed: {e}", level="warning")


def _print_summary(ctx: PythonPackageReleaseContext) -> None:
  log_and_print("=" * 50)
  log_and_print(f"🎉 Released Python Package v{ctx.new_version}")
  log_and_print("\n✅ Done:")
  log_and_print(f"   • {ctx.current_version} → {ctx.new_version}")
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

  paths = _resolve_paths()
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

  if not _bump_package_version(ctx):
    return
  if not _build_and_publish(ctx):
    return
  if not _finalize_submodule_git(ctx):
    return
  _sync_workspace_reference(ctx)
  _mirror_workspace_version(ctx)
  _print_summary(ctx)
