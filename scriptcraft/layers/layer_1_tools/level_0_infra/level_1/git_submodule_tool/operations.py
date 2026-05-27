from dataclasses import dataclass
from typing import Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    GitPrecheckResult,
    GitService,
    log_and_print,
    run_git_operation_with_precheck,
    list_submodule_paths,
)


@dataclass(frozen=True)
class SubmodulePrecheck:
    ok: bool
    reason: Optional[str] = None


def _git() -> GitService:
    return GitService()


def _precheck_repo_and_submodules(git: GitService) -> GitPrecheckResult:
    if not git.is_repo():
        return GitPrecheckResult(False, "❌ Not a Git repository")

    if not git.has_submodules():
        return GitPrecheckResult(True, "ℹ️ No submodules found", skip_body=True)

    return GitPrecheckResult(True)


def _run_with_precheck(*, verb: str, git: GitService, body) -> bool:
    return run_git_operation_with_precheck(
        operation_name=f"submodule {verb}",
        precheck=lambda: _precheck_repo_and_submodules(git),
        body=body,
        log=log_and_print,
        log_error=lambda msg: log_and_print(msg, level="error"),
    )


def sync_submodules() -> bool:
    git = _git()

    def _body() -> bool:
        log_and_print("🔄 Syncing submodules...")

        if not git._run_git("submodule sync").returncode == 0:
            log_and_print("❌ Failed to sync submodule URLs", level="error")
            return False

        if not git._run_git("submodule update --init --recursive").returncode == 0:
            log_and_print("❌ Failed to update submodules", level="error")
            return False

        log_and_print("✅ Submodules synced successfully")
        return True

    return _run_with_precheck(verb="sync", git=git, body=_body)


def pull_submodules() -> bool:
    git = _git()

    def _body() -> bool:
        log_and_print("📥 Pulling submodule changes...")

        result = git._run_git("submodule foreach 'git pull origin HEAD'")
        if result.returncode != 0:
            log_and_print("❌ Failed to pull submodules", level="error")
            return False

        log_and_print("✅ Submodules pulled successfully")
        return True

    return _run_with_precheck(verb="pull", git=git, body=_body)


def push_submodules() -> bool:
    git = _git()

    def _body() -> bool:
        log_and_print("📤 Pushing submodule changes...")

        for submodule in list_submodule_paths(git=git):
            log_and_print(f"📤 Queued push for submodule: {submodule}")

        result = git._run_git("submodule foreach 'git push origin HEAD'")
        if result.returncode != 0:
            log_and_print("❌ Failed to push submodules", level="error")
            return False

        log_and_print("✅ Submodules pushed successfully")
        return True

    return _run_with_precheck(verb="push", git=git, body=_body)


def update_submodules() -> bool:
    git = _git()

    def _body() -> bool:
        log_and_print("🔄 Updating submodules...")

        result = git._run_git("submodule update --remote --merge")
        if result.returncode != 0:
            log_and_print("❌ Failed to update submodules to latest", level="error")
            return False

        log_and_print("✅ Submodules updated successfully")
        return True

    return _run_with_precheck(verb="update", git=git, body=_body)
