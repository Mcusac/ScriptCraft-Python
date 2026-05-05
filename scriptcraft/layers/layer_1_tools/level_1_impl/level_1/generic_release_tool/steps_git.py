"""
Git repository release steps.

Refactored to use GitService as the single source of truth for all git operations.
"""

from pathlib import Path
from typing import Any

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print

from layers.layer_1_tools.level_1_impl.level_0.git_service import GitService


# ---------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------

def _git(repo_root: Path) -> GitService:
    """
    Create GitService bound to the provided repository root.
    """
    return GitService(repo_root=repo_root)


# ---------------------------------------------------------------------
# Git status check
# ---------------------------------------------------------------------

def check_git_status(*, repo_root: Path, **_: Any) -> None:
    """Check Git repository status."""
    log_and_print("🔍 Checking Git status...")

    git = _git(repo_root)

    if not git.is_repo():
        log_and_print("❌ Not a Git repository", level="error")
        return

    if git.has_changes():
        log_and_print("⚠️ Uncommitted changes found:", level="warning")
        log_and_print(git.status_porcelain(), level="warning")
        return

    log_and_print("✅ Git repository is clean")


# ---------------------------------------------------------------------
# Tag creation
# ---------------------------------------------------------------------

def create_git_tag(*, repo_root: Path, version: str, dry_run: bool, **_: Any) -> None:
    """Create a Git tag."""
    log_and_print(f"🏷️ Creating Git tag: v{version}")

    if dry_run:
        log_and_print("🔍 DRY RUN: Would create tag")
        return

    git = _git(repo_root)

    if not git.create_tag(version):
        log_and_print("❌ Tag creation failed", level="error")
        return

    log_and_print(f"✅ Git tag v{version} created")


# ---------------------------------------------------------------------
# Push to remote
# ---------------------------------------------------------------------

def push_to_remote(*, repo_root: Path, dry_run: bool, **_: Any) -> None:
    """Push to remote repository."""
    log_and_print("📤 Pushing to remote...")

    if dry_run:
        log_and_print("🔍 DRY RUN: Would push to remote")
        return

    git = _git(repo_root)

    # Push commits
    if not git.push():
        log_and_print("❌ Push failed", level="error")
        return

    # Push tags
    if not git.push_tags():
        log_and_print("❌ Tag push failed", level="error")
        return

    log_and_print("✅ Pushed to remote successfully")