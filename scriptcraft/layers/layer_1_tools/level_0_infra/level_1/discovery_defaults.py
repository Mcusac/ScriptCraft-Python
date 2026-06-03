"""
Composition-root defaults for tool discovery.

Wires filesystem scan paths and import prefixes so higher discovery/registry
modules stay free of hardcoded impl coupling.
"""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    DEFAULT_TOOL_MODULE_PREFIX,
    default_tool_discovery_paths,
)


def ensure_tools_discovered(registry: object) -> None:
    """Discover tools when registry has not been configured yet."""
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_8.registry import (
        UnifiedRegistry,
    )

    if not isinstance(registry, UnifiedRegistry):
        return

    if registry.is_discovered():
        return

    registry.discover_tools(
        paths=default_tool_discovery_paths(),
        module_prefix=DEFAULT_TOOL_MODULE_PREFIX,
    )
