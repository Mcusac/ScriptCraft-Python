"""
Git workspace operations.

Refactored to use GitService as the single source of truth for all git operations.

Design goals:
- No subprocess usage
- No duplicated git logic
- No dependency on probes or injected primitives
- Preserve existing public API signatures for safe migration
"""

from dataclasses import dataclass
from typing import Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.git_service import GitService


# ---------------------------------------------------------------------
# Precheck model
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class WorkspacePrecheck:
    ok: bool
    reason: Optional[str] = None


# ---------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------

def _get_git() -> GitService:
    """
    Centralized GitService instance.
    Uses current working directory as repo root.
    """
    return GitService()


def _precheck_repo(git: GitService) -> WorkspacePrecheck:
    """
    Validate repository state.
    """
    if not git.is_repo():
        return WorkspacePrecheck(False, "❌ Not a Git repository")
    return WorkspacePrecheck(True, None)


# ---------------------------------------------------------------------
# Public operations
# ---------------------------------------------------------------------

def push_workspace(
    *,
    is_git_repo=None,  # kept for backward compatibility (ignored)
    porcelain_status_has_changes=None,  # kept for backward compatibility (ignored)
    run_ok=None,  # kept for backward compatibility (ignored)
) -> bool:
    log_and_print("📤 Pushing workspace changes...")

    git = _get_git()

    pre = _precheck_repo(git)
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if git.has_changes():
        log_and_print("❌ Uncommitted changes found", level="error")
        return False

    if not git.push():
        log_and_print("❌ Failed to push commits", level="error")
        return False

    if not git.push_tags():
        log_and_print("❌ Failed to push tags", level="error")
        return False

    log_and_print("✅ Workspace pushed successfully")
    return True


def pull_workspace(
    *,
    is_git_repo=None,  # backward compatibility
    run_ok=None,  # backward compatibility
) -> bool:
    log_and_print("📥 Pulling workspace changes...")

    git = _get_git()

    pre = _precheck_repo(git)
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if not git.pull():
        log_and_print("❌ Failed to pull changes", level="error")
        return False

    log_and_print("✅ Workspace pulled successfully")
    return True


def check_status(
    *,
    is_git_repo=None,  # backward compatibility
    porcelain_status_has_changes=None,  # backward compatibility
) -> bool:
    log_and_print("🔍 Checking Git status...")

    git = _get_git()

    pre = _precheck_repo(git)
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if git.has_changes():
        log_and_print("⚠️ Uncommitted changes found:", level="warning")
        log_and_print(git.status_porcelain(), level="warning")
        return False

    log_and_print("✅ Git repository is clean")
    return True


def commit_changes(
    *,
    is_git_repo=None,  # backward compatibility
    porcelain_status_has_changes=None,  # backward compatibility
    run_ok=None,  # backward compatibility
    message: Optional[str],
) -> bool:
    log_and_print("💾 Committing changes...")

    git = _get_git()

    pre = _precheck_repo(git)
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if not git.has_changes():
        log_and_print("ℹ️ No changes to commit")
        return True

    if not git.add_all():
        log_and_print("❌ Failed to add changes", level="error")
        return False

    commit_message = message or "Auto-commit from ScriptCraft"

    if not git.commit(commit_message):
        log_and_print("❌ Commit failed", level="error")
        return False

    log_and_print("✅ Changes committed successfully")
    return True


def create_tag(
    *,
    is_git_repo=None,  # backward compatibility
    run_ok=None,  # backward compatibility
    version: Optional[str],
) -> bool:
    if not version:
        log_and_print("❌ Version required for tagging", level="error")
        return False

    log_and_print(f"🏷️ Creating Git tag: v{version}")

    git = _get_git()

    pre = _precheck_repo(git)
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if not git.create_tag(version):
        log_and_print(f"❌ Failed to create tag v{version}", level="error")
        return False

    log_and_print(f"✅ Git tag v{version} created")
    return True