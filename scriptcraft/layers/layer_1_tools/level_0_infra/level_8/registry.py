from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import ToolMetadata
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool, ToolDiscoveryEngine


class UnifiedRegistry:
    """
    Core registry orchestration layer.

    Responsibilities:
    - Tool lifecycle (class + instance caching)
    - Tool discovery coordination
    - Tool metadata storage
    """

    def __init__(self) -> None:
        self._tools: Dict[str, Type[BaseTool]] = {}
        self._tool_instances: Dict[str, BaseTool] = {}
        self._tool_metadata: Dict[str, ToolMetadata] = {}

        self._engine = ToolDiscoveryEngine()
        self._discovered: bool = False
        self._discovery_paths: List[Path] = []
        self._module_prefix: Optional[str] = None
        self._auto_discover: bool = False

    def configure_discovery(
        self,
        paths: List[Path],
        *,
        module_prefix: str,
        auto_discover: bool = True,
    ) -> None:
        """Set default discovery paths and import prefix for lazy discovery."""
        self._discovery_paths = list(paths)
        self._module_prefix = module_prefix
        self._auto_discover = auto_discover

    def is_discovered(self) -> bool:
        return self._discovered

    def discover_tools(
        self,
        paths: Optional[List[Path]] = None,
        *,
        module_prefix: Optional[str] = None,
    ) -> Dict[str, Type[BaseTool]]:
        resolved_paths = paths if paths is not None else self._discovery_paths
        prefix = module_prefix if module_prefix is not None else self._module_prefix

        if not resolved_paths:
            log_and_print("⚠️ No discovery paths configured; skipping tool discovery.")
            return {}

        if not prefix:
            raise ValueError(
                "module_prefix is required for tool discovery. "
                "Pass it to discover_tools() or call configure_discovery() first."
            )

        self._discovery_paths = list(resolved_paths)
        self._module_prefix = prefix
        found = self._engine.discover_tools(resolved_paths, module_prefix=prefix)

        self._tools.update(found)
        self._discovered = True

        return found

    def get_tool(
        self,
        tool_name: str,
        create_instance: bool = True,
    ) -> Optional[Union[Type[BaseTool], BaseTool]]:
        tool_class = self._tools.get(tool_name)
        if tool_class is None:
            return None

        if not create_instance:
            return tool_class

        if tool_name in self._tool_instances:
            return self._tool_instances[tool_name]

        try:
            instance = tool_class()
            self._tool_instances[tool_name] = instance
            return instance

        except Exception as e:
            log_and_print(f"⚠️ Failed to instantiate tool '{tool_name}': {e}")
            return None

    def run_tool(self, tool_name: str, **kwargs: Any) -> None:
        tool = self.get_tool(tool_name, create_instance=True)

        if tool is None:
            available = list(self._tools.keys())
            raise ValueError(
                f"Tool '{tool_name}' not found. Available tools: {available}"
            )

        tool.run(**kwargs)

    def get_tool_metadata(self, tool_name: str) -> Optional[ToolMetadata]:
        return self._tool_metadata.get(tool_name)

    def register_tool(
        self,
        name: str,
        tool_class: Type[BaseTool],
        metadata: Optional[ToolMetadata] = None,
    ) -> None:
        self._tools[name] = tool_class

        if metadata:
            self._tool_metadata[name] = metadata

        log_and_print(f"🔧 Registered tool: {name}")

    def refresh(self) -> None:
        self._tools.clear()
        self._tool_instances.clear()
        self._tool_metadata.clear()

        self._discovered = False

        if self._auto_discover and self._discovery_paths and self._module_prefix:
            self.discover_tools()

    def get_available_tools(self) -> Dict[str, Type[BaseTool]]:
        if not self._discovered and self._auto_discover:
            if self._discovery_paths and self._module_prefix:
                self.discover_tools()
        return dict(self._tools)


unified_registry = UnifiedRegistry()


def get_available_tools() -> Dict[str, Type[BaseTool]]:
    """Module-level helper for barrels and tool_registry imports."""
    return unified_registry.get_available_tools()
