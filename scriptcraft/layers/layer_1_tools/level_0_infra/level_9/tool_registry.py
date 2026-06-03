"""
Tool registry view over unified infra discovery.

Responsibilities:
- resolve tool classes by name
- list available tools with descriptions
"""

from typing import Dict, Optional, Type

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    ensure_tools_discovered,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import discover_tool_metadata
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool
from scriptcraft.layers.layer_1_tools.level_0_infra.level_8 import get_available_tools, unified_registry



def _description_for(tool_name: str) -> str:
    metadata = discover_tool_metadata(tool_name)
    if metadata and metadata.description:
        return metadata.description

    from scriptcraft.layers.layer_1_tools.level_0_infra.level_8.registry import (
        unified_registry,
    )

    tool = unified_registry.get_tool(tool_name, create_instance=True)
    if tool is None:
        return f"Tool: {tool_name}"
    if isinstance(tool, type):
        try:
            tool = tool()
        except Exception:
            return f"Tool: {tool_name}"
    description = getattr(tool, "description", None)
    if description:
        return str(description)
    return f"Tool: {tool_name}"


class ToolRegistry:
    """Read-only registry facade for discovered tool classes."""

    def get_tool(self, tool_name: str) -> Optional[Type[BaseTool]]:
        try:
            ensure_tools_discovered(unified_registry)
            tools = get_available_tools()
            return tools.get(tool_name)
        except Exception as e:
            log_and_print(f"❌ Failed to get tool '{tool_name}': {e}")
            return None

    def list_tools(self) -> Dict[str, str]:
        try:
            ensure_tools_discovered(unified_registry)
            tools = get_available_tools()
            return {tool_name: _description_for(tool_name) for tool_name in tools}
        except Exception as e:
            log_and_print(f"❌ Failed to list tools: {e}")
            return {}


registry = ToolRegistry()
