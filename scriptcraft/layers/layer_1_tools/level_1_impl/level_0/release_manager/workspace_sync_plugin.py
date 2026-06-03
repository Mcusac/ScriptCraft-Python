"""
Workspace Sync Plugin for Release Manager Tool.

Synchronizes the Python package submodule with the main workspace repository.
"""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
  log_and_print,
  find_workspace_root,
  submodule_path,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
  commit_and_push_submodule_changes,
  commit_workspace_submodule_ref,
)

def _sync_workspace(**kwargs) -> bool:
  log_and_print("🔄 Starting workspace synchronization...")
  workspace_root = find_workspace_root()

  if not submodule_path(workspace_root).exists():
    log_and_print("❌ Python package submodule not found", level="error")
    return False

  log_and_print("📦 Step 1: Updating python-package submodule...")
  if not commit_and_push_submodule_changes(
    workspace_root,
    commit_message=kwargs.get("commit_message"),
    interactive_message=kwargs.get("interactive", True),
  ):
    return False

  log_and_print("🏠 Step 2: Updating main workspace...")
  if not commit_workspace_submodule_ref(
    workspace_root,
    workspace_commit_message=kwargs.get("workspace_commit_message"),
    interactive_message=kwargs.get("interactive", True),
  ):
    return False

  log_and_print("✅ Workspace synchronization completed successfully!")
  return True


def _update_submodule(**kwargs) -> bool:
  return commit_and_push_submodule_changes(
    find_workspace_root(),
    commit_message=kwargs.get("commit_message"),
    interactive_message=kwargs.get("interactive", True),
  )


def workspace_sync_mode(input_paths, output_dir, domain=None, **kwargs):
  """Run workspace sync or submodule-only update."""
  _ = input_paths, output_dir, domain
  operation = kwargs.get("operation", "sync")

  if operation in ("sync", "workspace_sync"):
    return _sync_workspace(**kwargs)
  if operation == "submodule_update":
    return _update_submodule(**kwargs)

  log_and_print(f"❌ Unknown operation: {operation}", level="error")
  return False


class WorkspaceSyncPlugin:
  """Backward-compatible plugin class wrapper."""

  def __init__(self):
    self.name = "workspace_sync"
    self.description = "Synchronize workspace and submodule repositories"
    self.version = "1.0.0"

  def can_handle(self, operation: str) -> bool:
    return operation in ("sync", "workspace_sync", "submodule_update")

  def execute(self, operation: str, **kwargs) -> bool:
    if operation in ("sync", "workspace_sync"):
      return _sync_workspace(**kwargs)
    if operation == "submodule_update":
      return _update_submodule(**kwargs)
    log_and_print(f"❌ Unknown operation: {operation}", level="error")
    return False

  def get_operations(self) -> list:
    return ["sync", "workspace_sync", "submodule_update"]
