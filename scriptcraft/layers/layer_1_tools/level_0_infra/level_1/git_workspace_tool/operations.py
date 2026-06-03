"""
Git workspace operations.

Uses GitService as the single source of truth for all git operations.
"""

from dataclasses import dataclass
from typing import Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    GitPrecheckResult,
    GitService,
    log_and_print,
    run_git_operation_with_precheck,
)


@dataclass(frozen=True)
class WorkspacePrecheck:
    ok: bool
    reason: Optional[str] = None


def _get_git() -> GitService:
    return GitService()


def _precheck_repo(git: GitService) -> GitPrecheckResult:
    if not git.is_repo():
        return GitPrecheckResult(False, "❌ Not a Git repository")
    return GitPrecheckResult(True)


def _run_with_precheck(*, operation_name: str, git: GitService, body) -> bool:
    return run_git_operation_with_precheck(
        operation_name=operation_name,
        precheck=lambda: _precheck_repo(git),
        body=body,
        log=log_and_print,
        log_error=lambda msg: log_and_print(msg, level="error"),
    )


def push_workspace() -> bool:
    git = _get_git()

    def _body() -> bool:
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

    return _run_with_precheck(operation_name="workspace push", git=git, body=_body)


def pull_workspace() -> bool:
    git = _get_git()

    def _body() -> bool:
        if not git.pull():
            log_and_print("❌ Failed to pull commits", level="error")
            return False

        log_and_print("✅ Workspace pulled successfully")
        return True

    return _run_with_precheck(operation_name="workspace pull", git=git, body=_body)


def check_status() -> bool:
    git = _get_git()

    def _body() -> bool:
        status = git.status_porcelain()
        if status:
            log_and_print("📋 Workspace status:")
            log_and_print(status)
        else:
            log_and_print("✅ Working tree clean")
        return True

    return _run_with_precheck(operation_name="workspace status", git=git, body=_body)


def commit_changes(
    *,
    message: Optional[str] = None,
) -> bool:
    git = _get_git()

    def _body() -> bool:
        if not git.has_changes():
            log_and_print("ℹ️ No changes to commit")
            return True

        commit_message = message or "Automated workspace commit"
        if not git.commit_all(commit_message):
            log_and_print("❌ Failed to commit changes", level="error")
            return False

        log_and_print("✅ Workspace changes committed successfully")
        return True

    return _run_with_precheck(operation_name="workspace commit", git=git, body=_body)


def create_tag(
    *,
    version: Optional[str] = None,
) -> bool:
    git = _get_git()

    def _body() -> bool:
        if not version:
            log_and_print("❌ Version is required for tagging", level="error")
            return False

        if not git.create_tag(version):
            log_and_print("❌ Failed to create tag", level="error")
            return False

        log_and_print(f"✅ Tag v{version} created successfully")
        return True

    return _run_with_precheck(operation_name="workspace tag", git=git, body=_body)
