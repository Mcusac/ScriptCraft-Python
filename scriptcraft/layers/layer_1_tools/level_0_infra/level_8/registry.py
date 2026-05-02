from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_0.typed_plugin_store import get_typed_plugin
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_tools.level_0_infra.level_1.metadata import (
    ToolMetadata,
    PluginMetadata,
)

from layers.layer_1_tools.level_0_infra.level_7.discovery import ToolDiscoveryEngine


class UnifiedRegistry:
    """
    Core registry orchestration layer.

    Responsibilities:
    - Tool lifecycle (class + instance caching)
    - Tool discovery coordination
    - Plugin registration/access
    - Metadata storage
    """

    def __init__(self) -> None:
        # -------------------------
        # TOOL REGISTRY
        # -------------------------
        self._tools: Dict[str, Type[BaseTool]] = {}
        self._tool_instances: Dict[str, BaseTool] = {}
        self._tool_metadata: Dict[str, ToolMetadata] = {}

        # -------------------------
        # PLUGIN REGISTRY
        # -------------------------
        self._plugins: Dict[str, Dict[str, Any]] = {}
        self._plugin_metadata: Dict[str, PluginMetadata] = {}

        # -------------------------
        # DISCOVERY STATE
        # -------------------------
        self._engine = ToolDiscoveryEngine()
        self._discovered: bool = False
        self._discovery_paths: List[Path] = []
        self._auto_discover: bool = True

    # ============================================================
    # DISCOVERY
    # ============================================================

    def discover_tools(
        self,
        paths: Optional[List[Path]] = None
    ) -> Dict[str, Type[BaseTool]]:

        if paths is None:
            base = Path(__file__).parent.parent.parent
            paths = [base / "tools"]

        self._discovery_paths = paths
        found = self._engine.discover_tools(paths)

        self._tools.update(found)
        self._discovered = True

        return found

    # ============================================================
    # TOOL ACCESS LAYER
    # ============================================================

    def get_tool(
        self,
        tool_name: str,
        create_instance: bool = True
    ) -> Optional[Union[Type[BaseTool], BaseTool]]:

        tool_class = self._tools.get(tool_name)
        if tool_class is None:
            return None

        # --------------------------------------------------------
        # Return CLASS
        # --------------------------------------------------------
        if not create_instance:
            return tool_class

        # --------------------------------------------------------
        # Return CACHED INSTANCE if available
        # --------------------------------------------------------
        if tool_name in self._tool_instances:
            return self._tool_instances[tool_name]

        # --------------------------------------------------------
        # Create + CACHE INSTANCE
        # --------------------------------------------------------
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

    # ============================================================
    # METADATA LAYER
    # ============================================================

    def get_tool_metadata(self, tool_name: str) -> Optional[ToolMetadata]:
        return self._tool_metadata.get(tool_name)

    # ============================================================
    # REGISTRATION LAYER
    # ============================================================

    def register_tool(
        self,
        name: str,
        tool_class: Type[BaseTool],
        metadata: Optional[ToolMetadata] = None
    ) -> None:

        self._tools[name] = tool_class

        if metadata:
            self._tool_metadata[name] = metadata

        log_and_print(f"🔧 Registered tool: {name}")

    def register_plugin(
        self,
        plugin_type: str,
        name: str,
        plugin_class: Type,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:

        self._plugins.setdefault(plugin_type, {})[name] = plugin_class

        if metadata:
            self._plugin_metadata[name] = PluginMetadata(
                name=name,
                plugin_type=plugin_type,
                description=metadata.get("description", ""),
                version=metadata.get("version", "0.0.0"),
                tags=metadata.get("tags", []),
                metadata=metadata,
            )

        log_and_print(f"🔌 Registered plugin [{plugin_type}]: {name}")

    # ============================================================
    # PLUGIN ACCESS LAYER
    # ============================================================

    def get_plugin(self, plugin_type: str, name: str):
        return get_typed_plugin(self._plugins, plugin_type, name)

    def list_plugins(
        self,
        plugin_type: Optional[str] = None
    ) -> Dict[str, List[str]]:

        if plugin_type:
            return {
                plugin_type: list(self._plugins.get(plugin_type, {}).keys())
            }

        return {
            pt: list(plugins.keys())
            for pt, plugins in self._plugins.items()
        }

    # ============================================================
    # LIFECYCLE CONTROL
    # ============================================================

    def refresh(self) -> None:
        """
        Hard reset registry state.
        Keeps engine intact but clears runtime caches.
        """

        self._tools.clear()
        self._tool_instances.clear()
        self._tool_metadata.clear()

        self._discovered = False

        if self._auto_discover:
            self.discover_tools()