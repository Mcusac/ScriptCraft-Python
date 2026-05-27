"""Reusable git/submodule operations for release-manager plugins."""

from pathlib import Path
from typing import Optional

from scriptcraft.layers.layer_0_core.level_1 import run_command

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
  log_and_print,
  submodule_path,
)


def _run_ok(cmd: list[str], label: str, *, cwd: Path) -> bool:
  log_and_print(f"🔍 {label}...")
  try:
    result = run_command(cmd, check=False, cwd=cwd)
  except Exception as exc:
    log_and_print(f"❌ {label} - FAILED: {exc}", level="error")
    return False

  if int(result["returncode"]) == 0:
    log_and_print(f"✅ {label} - SUCCESS")
    return True

  stderr = (result.get("stderr") or "").strip()
  log_and_print(f"❌ {label} - FAILED", level="error")
  if stderr:
    log_and_print(f"Error: {stderr}", level="error")
  return False


def _run_str(cmd: list[str], label: str, *, cwd: Path) -> Optional[str]:
  log_and_print(f"🔄 {label}...")
  try:
    result = run_command(cmd, check=False, cwd=cwd)
  except Exception as exc:
    log_and_print(f"❌ {label} failed: {exc}", level="error")
    return None

  if int(result["returncode"]) == 0:
    log_and_print(f"✅ {label} completed")
    return (result.get("stdout") or "").strip()

  stderr = (result.get("stderr") or "").strip()
  log_and_print(f"❌ {label} failed", level="error")
  if stderr:
    log_and_print(f"Error output: {stderr}", level="error")
  return None


def git_status_porcelain(cwd: Path, label: str) -> Optional[str]:
  return _run_str(["git", "status", "--porcelain"], label, cwd=cwd)


def stage_all(cwd: Path, label: str = "Staging changes") -> bool:
  return _run_ok(["git", "add", "."], label, cwd=cwd)


def stage_path(cwd: Path, relative_path: str, label: str) -> bool:
  return _run_ok(["git", "add", str(relative_path)], label, cwd=cwd)


def commit_if_needed(
  cwd: Path,
  message: str,
  *,
  force: bool = False,
  status_label: str = "Checking git status",
) -> bool:
  status = git_status_porcelain(cwd, status_label)
  if status is None:
    return False
  if not status and not force:
    log_and_print("⚠️ No changes to commit", level="warning")
    return False
  if not stage_all(cwd):
    return False
  return _run_ok(["git", "commit", "-m", str(message)], "Committing", cwd=cwd)


def ensure_tag(cwd: Path, version: str) -> bool:
  existing = _run_str(["git", "tag", "-l", f"v{version}"], "Checking tag", cwd=cwd)
  if existing and existing.strip():
    return True
  return _run_ok(["git", "tag", f"v{version}"], "Creating tag", cwd=cwd)


def push_main_and_tag(cwd: Path, version: str, branch: str = "main") -> bool:
  if not _run_ok(["git", "push", "origin", str(branch)], "Pushing commits", cwd=cwd):
    return False
  return _run_ok(["git", "push", "origin", f"v{version}"], "Pushing tag", cwd=cwd)


def push_branch(cwd: Path, remote: str = "origin", branch: Optional[str] = None) -> bool:
  cmd = ["git", "push", str(remote)] if branch is None else ["git", "push", str(remote), str(branch)]
  return _run_ok(cmd, "Pushing changes", cwd=cwd)


def submodule_update_remote(workspace_root: Path) -> bool:
  rel = "implementations/python-package"
  return _run_ok(
    ["git", "submodule", "update", "--remote", rel],
    "Updating submodule reference",
    cwd=workspace_root,
  )


def resolve_commit_message(
  provided: Optional[str],
  prompt: str,
  default: str,
  *,
  interactive: bool = True,
) -> str:
  if provided:
    return provided
  if not interactive:
    return default
  try:
    user_input = input(prompt).strip()
    return user_input if user_input else default
  except Exception:
    return default


def commit_and_push_submodule_changes(
  workspace_root: Path,
  *,
  commit_message: str,
  interactive_message: bool = True,
  message_prompt: str = "Enter commit message for python-package submodule: ",
  default_message: str = "Update python-package submodule",
) -> bool:
  sub = submodule_path(workspace_root)
  if not sub.exists():
    log_and_print("❌ Python package submodule not found", level="error")
    return False

  status = git_status_porcelain(sub, "Checking submodule status")
  if status is None:
    return False

  if not status:
    log_and_print("ℹ️ No changes detected in submodule")
    return True

  log_and_print("📝 Found changes to commit in submodule:")
  log_and_print(status)

  if not stage_all(sub, "Adding changes"):
    return False

  msg = resolve_commit_message(
    commit_message,
    message_prompt,
    default_message,
    interactive=interactive_message,
  )
  if not _run_ok(["git", "commit", "-m", str(msg)], "Committing changes", cwd=sub):
    return False

  if not push_branch(sub):
    return False

  log_and_print("✅ Submodule updated successfully!")
  return True


def commit_workspace_submodule_ref(
  workspace_root: Path,
  *,
  workspace_commit_message: Optional[str] = None,
  interactive_message: bool = True,
) -> bool:
  if not submodule_update_remote(workspace_root):
    return False

  status = git_status_porcelain(workspace_root, "Checking workspace status")
  if status is None:
    return False

  rel = "implementations/python-package"
  if rel not in status:
    log_and_print("ℹ️ No submodule updates detected")
    return True

  if not stage_path(workspace_root, rel, "Staging submodule"):
    return False

  msg = resolve_commit_message(
    workspace_commit_message,
    "Enter commit message for main workspace: ",
    "Update submodule reference",
    interactive=interactive_message,
  )
  if not _run_ok(["git", "commit", "-m", str(msg)], "Committing workspace", cwd=workspace_root):
    return False

  if not push_branch(workspace_root):
    return False

  log_and_print("✅ Workspace updated successfully!")
  return True
