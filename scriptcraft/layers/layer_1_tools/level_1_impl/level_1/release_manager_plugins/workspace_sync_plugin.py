"""
🔄 Workspace Sync Plugin for Release Manager

This plugin handles synchronization between the Python package submodule
and the main workspace repository.
"""

from pathlib import Path
from typing import Optional

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print

from layers.layer_1_tools.level_1_impl.level_0.subprocess.runner import run_str, run_ok


# ============================================================
# 🔧 Helpers
# ============================================================

def _get_workspace_root() -> Path:
    """Locate workspace root by searching for config.yaml."""
    current_dir = Path.cwd()

    for parent in [current_dir] + list(current_dir.parents):
        if (parent / "config.yaml").exists():
            return parent

    return current_dir


def _resolve_commit_message(
    provided: Optional[str],
    prompt: str,
    default: str,
) -> str:
    """
    Preserve original behavior:
    - Use provided message if given
    - Otherwise prompt user
    - Fallback to default if input empty
    """
    if provided:
        return provided

    try:
        user_input = input(prompt).strip()
        return user_input if user_input else default
    except Exception:
        return default


# ============================================================
# 🚀 Entry Point
# ============================================================

def run_mode(input_paths, output_dir, domain=None, **kwargs):
    """
    Run workspace sync mode.

    Operations:
    - sync / workspace_sync
    - submodule_update
    """
    operation = kwargs.get("operation", "sync")

    if operation in ["sync", "workspace_sync"]:
        return _sync_workspace(**kwargs)

    if operation == "submodule_update":
        return _update_submodule(**kwargs)

    log_and_print(f"❌ Unknown operation: {operation}", level="error")
    return False


# ============================================================
# 🔄 Core Logic
# ============================================================

def _sync_workspace(**kwargs) -> bool:
    """Full sync: submodule + workspace."""
    log_and_print("🔄 Starting workspace synchronization...")

    workspace_root = _get_workspace_root()
    submodule_path = workspace_root / "implementations" / "python-package"

    if not submodule_path.exists():
        log_and_print("❌ Python package submodule not found", level="error")
        return False

    # Step 1
    log_and_print("📦 Step 1: Updating python-package submodule...")
    if not _update_submodule(**kwargs):
        return False

    # Step 2
    log_and_print("🏠 Step 2: Updating main workspace...")
    if not _update_workspace_reference(**kwargs):
        return False

    log_and_print("✅ Workspace synchronization completed successfully!")
    return True


def _update_submodule(**kwargs) -> bool:
    """Update submodule repository."""
    submodule_path = _get_workspace_root() / "implementations" / "python-package"

    status = run_str(
        "git status --porcelain",
        "Checking submodule status",
        cwd=submodule_path,
    )

    if status is None:
        return False

    if status:
        log_and_print("📝 Found changes to commit in submodule:")
        log_and_print(status)

        if not run_ok("git add .", "Adding changes", cwd=submodule_path):
            return False

        commit_message = _resolve_commit_message(
            kwargs.get("commit_message"),
            "Enter commit message for python-package submodule: ",
            "Update python-package submodule",
        )

        if not run_ok(
            f'git commit -m "{commit_message}"',
            "Committing changes",
            cwd=submodule_path,
        ):
            return False

        if not run_ok("git push", "Pushing changes", cwd=submodule_path):
            return False

        log_and_print("✅ Submodule updated successfully!")
    else:
        log_and_print("ℹ️ No changes detected in submodule")

    return True


def _update_workspace_reference(**kwargs) -> bool:
    """Update submodule reference in main workspace."""
    workspace_root = _get_workspace_root()

    if not run_ok(
        "git submodule update --remote implementations/python-package",
        "Updating submodule reference",
        cwd=workspace_root,
    ):
        return False

    status = run_str(
        "git status --porcelain",
        "Checking workspace status",
        cwd=workspace_root,
    )

    if status is None:
        return False

    if "implementations/python-package" in status:
        if not run_ok(
            "git add implementations/python-package",
            "Staging submodule",
            cwd=workspace_root,
        ):
            return False

        commit_message = _resolve_commit_message(
            kwargs.get("workspace_commit_message"),
            "Enter commit message for main workspace: ",
            "Update submodule reference",
        )

        if not run_ok(
            f'git commit -m "{commit_message}"',
            "Committing workspace",
            cwd=workspace_root,
        ):
            return False

        if not run_ok("git push", "Pushing workspace", cwd=workspace_root):
            return False

        log_and_print("✅ Workspace updated successfully!")
    else:
        log_and_print("ℹ️ No submodule updates detected")

    return True


# ============================================================
# 🧩 Plugin Class (Backward Compatibility)
# ============================================================

class WorkspaceSyncPlugin:
    """Plugin for synchronizing workspace and submodule repositories."""

    def __init__(self):
        self.name = "workspace_sync"
        self.description = "🔄 Synchronize workspace and submodule repositories"
        self.version = "1.0.0"

    def can_handle(self, operation: str) -> bool:
        return operation in ["sync", "workspace_sync", "submodule_update"]

    def execute(self, operation: str, **kwargs) -> bool:
        if operation in ["sync", "workspace_sync"]:
            return _sync_workspace(**kwargs)

        if operation == "submodule_update":
            return _update_submodule(**kwargs)

        log_and_print(f"❌ Unknown operation: {operation}", level="error")
        return False

    def get_help(self) -> str:
        return """
            Workspace Sync Plugin
            ====================

            Synchronizes the Python package submodule with the main workspace.

            Operations:
            - sync / workspace_sync
            - submodule_update

            Options:
            - commit_message
            - workspace_commit_message
            """

    def get_operations(self) -> list:
        return ["sync", "workspace_sync", "submodule_update"]