from dataclasses import dataclass
from typing import Callable, Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_tools.level_1_impl.level_0.subprocess.runner import run_ok
from layers.layer_1_tools.level_1_impl.level_0.git_submodule_tool.submodules import list_submodules
from layers.layer_1_tools.level_1_impl.level_1.git.probes import (
    has_submodules,
    is_git_repo,
)


@dataclass(frozen=True)
class SubmodulePrecheck:
    ok: bool
    reason: Optional[str] = None


def _precheck_repo_and_submodules() -> SubmodulePrecheck:
    if not is_git_repo():
        return SubmodulePrecheck(False, "❌ Not a Git repository")

    if not has_submodules():
        return SubmodulePrecheck(True, "ℹ️ No submodules found")

    return SubmodulePrecheck(True, None)


def _run_with_precheck(
    *,
    verb: str,
    body: Callable[[], bool],
) -> bool:
    log_and_print(f"🚀 Starting Git submodule {verb} operation...")

    pre = _precheck_repo_and_submodules()
    if not pre.ok:
        log_and_print(pre.reason or "❌ Precheck failed", level="error")
        return False

    if pre.reason:
        log_and_print(pre.reason)
        return True

    return body()


def sync_submodules() -> bool:
    def _body() -> bool:
        log_and_print("🔄 Syncing submodules...")
        if not run_ok("git submodule sync", "Syncing submodule URLs"):
            return False
        if not run_ok("git submodule update --init --recursive", "Updating submodules"):
            return False
        log_and_print("✅ Submodules synced successfully")
        return True

    return _run_with_precheck(verb="sync", body=_body)


def pull_submodules() -> bool:
    def _body() -> bool:
        log_and_print("📥 Pulling submodule changes...")
        if not run_ok("git submodule foreach 'git pull origin HEAD'", "Pulling submodules"):
            return False
        log_and_print("✅ Submodules pulled successfully")
        return True

    return _run_with_precheck(verb="pull", body=_body)


def push_submodules() -> bool:
    def _body() -> bool:
        log_and_print("📤 Pushing submodule changes...")

        # Enumerate for nicer per-submodule logging, but run the foreach once.
        submodules = list_submodules()
        for submodule in submodules:
            log_and_print(f"📤 Queued push for submodule: {submodule}")

        if not run_ok("git submodule foreach 'git push origin HEAD'", "Pushing submodules"):
            return False

        log_and_print("✅ Submodules pushed successfully")
        return True

    return _run_with_precheck(verb="push", body=_body)


def update_submodules() -> bool:
    def _body() -> bool:
        log_and_print("🔄 Updating submodules...")
        if not run_ok("git submodule update --remote --merge", "Updating submodules to latest"):
            return False
        log_and_print("✅ Submodules updated successfully")
        return True

    return _run_with_precheck(verb="update", body=_body)

