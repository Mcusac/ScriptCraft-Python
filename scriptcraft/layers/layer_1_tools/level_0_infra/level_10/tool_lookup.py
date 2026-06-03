"""
Tool lookup abstraction for dispatching ScriptCraft tools.

Contract: lookups return tool classes (not instances). The dispatcher owns
instantiation so there is a single place where construction happens.
"""

from dataclasses import dataclass
from typing import Optional, Protocol, Type

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    ensure_tools_discovered,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool
from scriptcraft.layers.layer_1_tools.level_0_infra.level_8 import unified_registry


class ToolLookup(Protocol):
    def get_tool_class(self, tool_name: str) -> Optional[Type[BaseTool]]:
        ...


@dataclass(frozen=True)
class InfraRegistryToolLookup:
    """Adapter around the infra unified registry for dispatch resolution."""

    def get_tool_class(self, tool_name: str) -> Optional[Type[BaseTool]]:
        ensure_tools_discovered(unified_registry)
        tools = unified_registry.get_available_tools()
        return tools.get(tool_name)
