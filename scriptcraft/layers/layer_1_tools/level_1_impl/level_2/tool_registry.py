"""
Tool dispatcher for managing and running tools in the scriptcraft/tools directory.

This module provides functionality to discover and dispatch tools using a
consistent interface and error handling. It now uses the unified tool interface
from the tools package.
"""

from typing import Any, Dict, Optional, Type

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_pypi.level_0_infra.level_6.base_tool import BaseTool
from layers.layer_1_pypi.level_0_infra.level_7.registry import discover_tool_metadata, get_available_tools

from layers.layer_1_pypi.level_1_impl.level_1.tooling_dispatcher import dispatch_tool


class ToolRegistry:
    """
    Registry for managing available tools.
    
    This class now wraps the unified tool interface from tools/__init__.py
    to maintain backward compatibility.
    """
    
    def __init__(self) -> None:
        # Use the unified tool discovery system
        pass
    
    def get_tool(self, tool_name: str) -> Optional[Type[BaseTool]]:
        """
        Get a tool class by name.
        
        Args:
            tool_name: Name of the tool to get
        
        Returns:
            Optional[Type[BaseTool]]: Tool class if found, None otherwise
        """
        try:
            tools = get_available_tools()
            return tools.get(tool_name)
        except Exception as e:
            log_and_print(f"❌ Failed to get tool '{tool_name}': {e}")
            return None
    
    def list_tools(self) -> Dict[str, str]:
        """
        Get a dictionary of available tools.
        
        Returns:
            Dict[str, str]: Dictionary mapping tool names to descriptions
        """
        try:
            tools = get_available_tools()
            # Return tool names mapped to descriptions for backward compatibility
            result = {}
            for tool_name, tool_instance in tools.items():
                metadata = discover_tool_metadata(tool_name)
                result[tool_name] = metadata.get("description", f"Tool: {tool_name}")
            return result
        except Exception as e:
            log_and_print(f"❌ Failed to list tools: {e}")
            return {}

# Create singleton registry
registry = ToolRegistry()

def dispatch_tool(tool_name: str, args: Any) -> None:
    """
    Dispatch a tool based on CLI args.
    
    Args:
        tool_name: Name of the tool to run
        args: Parsed command line arguments
    """
    # Backward-compatible shim; implementation lives in tooling/dispatcher.py
    return dispatch_tool(tool_name, args)
