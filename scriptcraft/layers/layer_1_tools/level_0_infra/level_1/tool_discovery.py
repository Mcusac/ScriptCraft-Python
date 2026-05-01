
from typing import Any, Callable, Iterable, Optional

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print


def discover_and_merge_tools(
    config: Any,
    discovered_tool_names: Iterable[str],
    *,
    describe_tool: Optional[Callable[[str], Optional[str]]] = None,
) -> None:
    """
    Merge discovered tools into `config.tools` without performing discovery itself.

    This is a focused service layer function: orchestration is responsible for
    tool discovery and for providing any metadata/description provider.
    """
    try:
        for name in discovered_tool_names:
            if name not in config.tools:
                description = describe_tool(name) if describe_tool else None
                description = description or name

                config.tools[name] = {
                    "tool_name": name,
                    "description": description,
                }

    except Exception as e:
        log_and_print(f"⚠️ Could not discover tools: {e}", level="warning")