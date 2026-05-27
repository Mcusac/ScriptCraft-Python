"""Workspace and submodule synchronization workflows."""

from pathlib import Path
from typing import Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print, GitService


def _find_workspace_root(start: Optional[Path] = None) -> Path:
  current = start or Path.cwd()
  for parent in [current, *current.parents]:
    if (parent / "config.yaml").exists():
      return parent
  return current


def run_git_sync_workflow(
  *,
  commit_message: str = "Auto-commit: Automated sync",
  repo_root: Optional[Path] = None,
) -> bool:
  """
  Sync submodules (if any), commit workspace changes, and push.

  Mirrors legacy release_cli git-sync behavior using GitService only.
  """
  root = repo_root or _find_workspace_root()
  git = GitService(repo_root=root)

  if not git.is_repo():
    log_and_print("Not a Git repository", level="error")
    return False

  log_and_print("Syncing submodules...")
  if git.has_submodules():
    sync_result = git._run_git("submodule update --init --recursive")
    if sync_result.returncode != 0:
      log_and_print(f"Submodule sync failed: {sync_result.stderr}", level="error")
      return False

  log_and_print("Committing workspace changes...")
  if git.has_changes():
    if not git.add_all():
      return False
    if not git.commit(commit_message):
      return False
  else:
    log_and_print("No changes to commit")

  log_and_print("Pushing workspace...")
  return git.push()


def run_git_status_workflow(*, repo_root: Optional[Path] = None) -> bool:
  root = repo_root or _find_workspace_root()
  git = GitService(repo_root=root)
  if not git.is_repo():
    log_and_print("Not a Git repository", level="error")
    return False
  status = git.status_porcelain()
  if status:
    log_and_print("Uncommitted changes:")
    log_and_print(status)
  else:
    log_and_print("Git repository is clean")
  return True
