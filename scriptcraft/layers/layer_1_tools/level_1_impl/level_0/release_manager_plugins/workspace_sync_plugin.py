"""
🔄 Workspace Sync Plugin for Release Manager

This plugin handles synchronization between the Python package submodule and the main workspace repository.
It replicates the functionality from the PowerShell scripts for cross-platform compatibility.
"""

import os
import subprocess

from pathlib import Path

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print


def _get_workspace_root():
    """Get the workspace root directory by looking for config.yaml."""
    current_dir = Path.cwd()
    
    # Look for config.yaml in current directory or parents
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / "config.yaml").exists():
            return parent
    
    # Fallback to current directory
    return current_dir


def run_mode(input_paths, output_dir, domain=None, **kwargs):
    """
    Run the workspace sync mode.
    
    This function replicates the functionality from the PowerShell scripts:
    - github_push.ps1: Updates submodule and workspace
    - release_all.ps1: Orchestrates the full workflow
    
    Args:
        input_paths: List of input file paths (not used)
        output_dir: Output directory (not used)
        domain: Domain context (not used)
        **kwargs: Additional arguments including:
            - operation: Operation to perform (sync, submodule_update)
            - commit_message: Commit message for submodule
            - workspace_commit_message: Commit message for workspace
    """
    operation = kwargs.get('operation', 'sync')
    
    if operation in ['sync', 'workspace_sync']:
        return _sync_workspace(**kwargs)
    elif operation == 'submodule_update':
        return _update_submodule(**kwargs)
    else:
        log_and_print(f"❌ Unknown operation: {operation}", level="error")
        return False


def _sync_workspace(**kwargs):
    """Synchronize the entire workspace (submodule + main repo)."""
    log_and_print("🔄 Starting workspace synchronization...")
    
    # Get paths
    workspace_root = _get_workspace_root()
    submodule_path = workspace_root / "implementations" / "python-package"
    
    if not submodule_path.exists():
        log_and_print("❌ Python package submodule not found", level="error")
        return False
    
    # Step 1: Update submodule repository
    log_and_print("📦 Step 1: Updating python-package submodule...")
    if not _update_submodule(**kwargs):
        return False
    
    # Step 2: Update main workspace
    log_and_print("🏠 Step 2: Updating main workspace...")
    if not _update_workspace_reference(**kwargs):
        return False
    
    log_and_print("✅ Workspace synchronization completed successfully!")
    return True


def _update_submodule(**kwargs):
    """Update the Python package submodule repository."""
    try:
        # Change to submodule directory
        submodule_path = _get_workspace_root() / "implementations" / "python-package"
        os.chdir(submodule_path)
        
        # Check git status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, encoding='utf-8', errors='replace', check=True
        )
        
        if result.stdout.strip():
            log_and_print("📝 Found changes to commit in submodule:")
            log_and_print(result.stdout.strip())
            
            # Add all changes
            log_and_print("➕ Adding changes...")
            subprocess.run(["git", "add", "."], check=True)
            
            # Get commit message
            commit_message = kwargs.get('commit_message')
            if not commit_message:
                commit_message = input("Enter commit message for python-package submodule: ")
            
            # Commit
            log_and_print(f"💾 Committing with message: '{commit_message}'")
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            
            # Push
            log_and_print("🚀 Pushing to remote...")
            subprocess.run(["git", "push"], check=True)
            
            log_and_print("✅ Submodule updated successfully!")
        else:
            log_and_print("ℹ️ No changes detected in submodule")
        
        return True
        
    except subprocess.CalledProcessError as e:
        log_and_print(f"❌ Git operation failed: {e}", level="error")
        return False
    except Exception as e:
        log_and_print(f"❌ Submodule update failed: {e}", level="error")
        return False


def _update_workspace_reference(**kwargs):
    """Update the submodule reference in the main workspace."""
    try:
        # Return to workspace root
        workspace_root = _get_workspace_root()
        os.chdir(workspace_root)
        
        # Update submodule reference
        log_and_print("🔄 Updating submodule reference...")
        subprocess.run(
            ["git", "submodule", "update", "--remote", "implementations/python-package"],
            check=True
        )
        
        # Check if submodule was updated
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, encoding='utf-8', errors='replace', check=True
        )
        
        if "implementations/python-package" in result.stdout:
            log_and_print("📝 Submodule reference updated, committing...")
            
            # Add submodule changes
            subprocess.run(["git", "add", "implementations/python-package"], check=True)
            
            # Get commit message
            commit_message = kwargs.get('workspace_commit_message')
            if not commit_message:
                commit_message = input("Enter commit message for main workspace: ")
            
            # Commit
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            
            # Push
            log_and_print("🚀 Pushing workspace changes...")
            subprocess.run(["git", "push"], check=True)
            
            log_and_print("✅ Workspace updated successfully!")
        else:
            log_and_print("ℹ️ No submodule updates detected")
        
        return True
        
    except subprocess.CalledProcessError as e:
        log_and_print(f"❌ Git operation failed: {e}", level="error")
        return False
    except Exception as e:
        log_and_print(f"❌ Workspace update failed: {e}", level="error")
        return False


# Legacy class interface for backward compatibility
class WorkspaceSyncPlugin:
    """Plugin for synchronizing workspace and submodule repositories."""
    
    def __init__(self):
        self.name = "workspace_sync"
        self.description = "🔄 Synchronize workspace and submodule repositories"
        self.version = "1.0.0"
    
    def can_handle(self, operation: str) -> bool:
        """Check if this plugin can handle the given operation."""
        return operation in ["sync", "workspace_sync", "submodule_update"]
    
    def execute(self, operation: str, **kwargs) -> bool:
        """Execute the workspace sync operation."""
        if operation in ["sync", "workspace_sync"]:
            return _sync_workspace(**kwargs)
        elif operation == "submodule_update":
            return _update_submodule(**kwargs)
        else:
            log_and_print(f"❌ Unknown operation: {operation}", level="error")
            return False
    
    def get_help(self) -> str:
        """Get help information for this plugin."""
        return """
Workspace Sync Plugin
====================

This plugin synchronizes the Python package submodule with the main workspace repository.

Operations:
- sync / workspace_sync: Full workspace synchronization (submodule + main repo)
- submodule_update: Update only the submodule repository

Options:
- commit_message: Commit message for submodule changes
- workspace_commit_message: Commit message for workspace changes

Examples:
  release_manager workspace_sync sync
  release_manager workspace_sync submodule_update --commit-message "Update package"
        """
    
    def get_operations(self) -> list:
        """Get list of supported operations."""
        return ["sync", "workspace_sync", "submodule_update"]
