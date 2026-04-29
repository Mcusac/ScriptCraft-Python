
import subprocess
from dataclasses import dataclass
from typing import Callable, Optional

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print


@dataclass(frozen=True)
class WorkspacePrecheck:
    ok: bool
    reason: Optional[str] = None


def _precheck_repo(*, is_git_repo: Callable[[], bool]) -> WorkspacePrecheck:
    if not is_git_repo():
        return WorkspacePrecheck(False, "❌ Not a Git repository")
    return WorkspacePrecheck(True, None)


def push_workspace(
    *,
    is_git_repo: Callable[[], bool],
    porcelain_status_has_changes: Callable[[], bool],
    run_ok: Callable[[str, str], bool],
) -> bool:
    log_and_print("📤 Pushing workspace changes...")

    pre = _precheck_repo(is_git_repo=is_git_repo)
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if porcelain_status_has_changes():
        log_and_print("❌ Uncommitted changes found", level="error")
        return False

    if not run_ok("git push", "Pushing commits"):
        return False

    if not run_ok("git push --tags", "Pushing tags"):
        return False

    log_and_print("✅ Workspace pushed successfully")
    return True


def pull_workspace(*, is_git_repo: Callable[[], bool], run_ok: Callable[[str, str], bool]) -> bool:
    log_and_print("📥 Pulling workspace changes...")

    pre = _precheck_repo(is_git_repo=is_git_repo)
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if not run_ok("git pull", "Pulling changes"):
        return False

    log_and_print("✅ Workspace pulled successfully")
    return True


def check_status(*, is_git_repo: Callable[[], bool], porcelain_status_has_changes: Callable[[], bool]) -> bool:
    log_and_print("🔍 Checking Git status...")

    pre = _precheck_repo(is_git_repo=is_git_repo)
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if porcelain_status_has_changes():
        log_and_print("⚠️ Uncommitted changes found:", level="warning")
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        log_and_print(result.stdout, level="warning")
        return False

    log_and_print("✅ Git repository is clean")
    return True


def commit_changes(
    *,
    is_git_repo: Callable[[], bool],
    porcelain_status_has_changes: Callable[[], bool],
    run_ok: Callable[[str, str], bool],
    message: Optional[str],
) -> bool:
    log_and_print("💾 Committing changes...")

    pre = _precheck_repo(is_git_repo=is_git_repo)
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if not porcelain_status_has_changes():
        log_and_print("ℹ️ No changes to commit")
        return True

    if not run_ok("git add .", "Adding changes"):
        return False

    commit_message = message or "Auto-commit from ScriptCraft"
    if not run_ok(f'git commit -m \"{commit_message}\"', "Committing changes"):
        return False

    log_and_print("✅ Changes committed successfully")
    return True


def create_tag(*, is_git_repo: Callable[[], bool], run_ok: Callable[[str, str], bool], version: Optional[str]) -> bool:
    if not version:
        log_and_print("❌ Version required for tagging", level="error")
        return False

    log_and_print(f"🏷️ Creating Git tag: v{version}")

    pre = _precheck_repo(is_git_repo=is_git_repo)
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if not run_ok(f"git tag v{version}", f"Creating tag v{version}"):
        return False

    log_and_print(f"✅ Git tag v{version} created")
    return True

