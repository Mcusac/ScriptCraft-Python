from dataclasses import dataclass
from typing import Optional

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print

from layers.layer_1_tools.level_1_impl.level_0.git_service import GitService
from layers.layer_1_tools.level_1_impl.level_0.git_submodule_tool.submodules import list_submodules


# ---------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class SubmodulePrecheck:
    ok: bool
    reason: Optional[str] = None


# ---------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------

def _git() -> GitService:
    """
    Central GitService instance for submodule operations.
    """
    return GitService()


def _precheck_repo_and_submodules(git: GitService) -> SubmodulePrecheck:
    """
    Validate repo and submodule state.

    Preserves original semantics:
    - If not a git repo → hard fail
    - If no submodules → allowed, but informational
    """
    if not git.is_repo():
        return SubmodulePrecheck(False, "❌ Not a Git repository")

    if not git.has_submodules():
        return SubmodulePrecheck(True, "ℹ️ No submodules found")

    return SubmodulePrecheck(True, None)


def _run_with_precheck(
    *,
    verb: str,
    git: GitService,
    body,
) -> bool:
    """
    Shared execution wrapper preserving original flow.
    """
    log_and_print(f"🚀 Starting Git submodule {verb} operation...")

    pre = _precheck_repo_and_submodules(git)

    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if pre.reason:
        log_and_print(pre.reason)
        return True

    return body()


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

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

        # Preserve original per-submodule logging behavior
        submodules = list_submodules()
        for submodule in submodules:
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