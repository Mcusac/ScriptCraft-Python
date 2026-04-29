"""
Plugin registry for Release Manager Tool.

This module provides a registry system for managing different release workflow plugins.
"""

from typing import Any, Dict, List, Optional, Callable


def _safe_print(message: str) -> None:
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("ascii", "replace").decode())


class ReleaseWorkflowRegistry:
    """Registry for managing release workflows keyed by `mode` name."""
    
    def __init__(self) -> None:
        self._workflows: Dict[str, Callable] = {}
        self._workflow_info: Dict[str, Dict[str, Any]] = {}
    
    def register_workflow(self, mode: str, workflow: Callable, info: Optional[Dict[str, Any]] = None) -> None:
        """
        Register a release workflow with the registry.
        
        Args:
            mode: Release mode name (e.g., 'python_package', 'workspace')
            workflow: Workflow callable to register
            info: Optional workflow information dictionary
        """
        self._workflows[mode] = workflow
        self._workflow_info[mode] = info or {}
        
        _safe_print(f"🔌 Registered release workflow: {mode}")
    
    def get_workflow(self, mode: str) -> Optional[Callable]:
        """
        Get a workflow by mode name.
        
        Args:
            mode: Release mode name
            
        Returns:
            Workflow callable or None if not found
        """
        return self._workflows.get(mode)
    
    def list_workflows(self) -> List[str]:
        """
        List all registered workflow modes.
        
        Returns:
            List of workflow mode names
        """
        return list(self._workflows.keys())
    
    def get_workflow_info(self, mode: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a workflow.
        
        Args:
            mode: Release mode name
            
        Returns:
            Workflow information dictionary or None if not found
        """
        return self._workflow_info.get(mode)
    
    def get_workflows_by_feature(self, feature: str) -> List[str]:
        """
        Get workflows that support a specific feature.
        
        Args:
            feature: Feature name (e.g., 'supports_pypi', 'supports_git')
            
        Returns:
            List of workflow modes that support the feature
        """
        supported_plugins = []
        for name, info in self._workflow_info.items():
            if info.get(feature, False):
                supported_plugins.append(name)
        return supported_plugins
    
    def get_workflows_by_version_type(self, version_type: str) -> List[str]:
        """
        Get workflows that support a specific version type.
        
        Args:
            version_type: Version type (e.g., 'major', 'minor', 'patch')
            
        Returns:
            List of workflow modes that support the version type
        """
        supported_plugins = []
        for name, info in self._workflow_info.items():
            version_types = info.get('version_types', [])
            if version_type in version_types:
                supported_plugins.append(name)
        return supported_plugins
    
    def unregister_workflow(self, mode: str) -> bool:
        """
        Unregister a workflow from the registry.
        
        Args:
            mode: Release mode name to unregister
            
        Returns:
            True if workflow was unregistered, False if not found
        """
        if mode in self._workflows:
            del self._workflows[mode]
            del self._workflow_info[mode]
            _safe_print(f"🔌 Unregistered release workflow: {mode}")
            return True
        return False
    
    def clear_workflows(self) -> None:
        """Clear all registered workflows."""
        self._workflows.clear()
        self._workflow_info.clear()
        _safe_print("🔌 Cleared all release workflows")
    
    def workflow_count(self) -> int:
        """
        Get the number of registered workflows.
        
        Returns:
            Number of workflows
        """
        return len(self._workflows)
    
    def has_workflow(self, mode: str) -> bool:
        """
        Check if a workflow is registered.
        
        Args:
            mode: Release mode name to check
            
        Returns:
            True if workflow is registered, False otherwise
        """
        return mode in self._workflows
