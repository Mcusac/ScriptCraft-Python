"""
Tool lookup abstraction for dispatching ScriptCraft tools.

Contract: lookups return tool classes (not instances). The dispatcher owns
instantiation so we have a single, testable place where construction happens.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Protocol, Type

from layers.layer_1_pypi.level_0_infra.level_6.base_tool import BaseTool
from layers.layer_1_pypi.level_0_infra.level_7.registry import get_available_tools


class ToolLookup(Protocol):
    def get_tool_class(self, tool_name: str) -> Optional[Type[BaseTool]]:
        ...

    def list_tool_descriptions(self) -> Dict[str, str]:
        ...


@dataclass(frozen=True)
class InfraRegistryToolLookup:
    """
    Adapter around the infra unified registry convenience functions.
    """

    def get_tool_class(self, tool_name: str) -> Optional[Type[BaseTool]]:
        tools = get_available_tools()
        return tools.get(tool_name)

    def list_tool_descriptions(self) -> Dict[str, str]:
        tools = get_available_tools()
        # Descriptions are handled elsewhere (metadata discovery) to keep this lookup small.
        return {name: f"Tool: {name}" for name in tools.keys()}

