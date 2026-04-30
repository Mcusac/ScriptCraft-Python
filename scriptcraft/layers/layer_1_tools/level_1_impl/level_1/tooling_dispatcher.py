"""
Tool dispatch execution.

Responsibilities:
- resolve a tool class by name (via ToolLookup)
- instantiate the tool
- map CLI args to `run()` kwargs
- execute with consistent error handling/logging
"""

from typing import Any, Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_tools.level_1_impl.level_0.tooling.arg_mapping import build_run_kwargs_from_args
from layers.layer_1_tools.level_1_impl.level_0.tooling.tool_lookup import InfraRegistryToolLookup, ToolLookup


def dispatch_tool(tool_name: str, args: Any, *, lookup: Optional[ToolLookup] = None) -> None:
    effective_lookup = lookup or InfraRegistryToolLookup()

    try:
        tool_class = effective_lookup.get_tool_class(tool_name)
        if tool_class is None:
            raise ValueError(f"Tool '{tool_name}' not found.")

        tool_instance = tool_class()
        run_kwargs = build_run_kwargs_from_args(args)
        tool_instance.run(**run_kwargs)
    except Exception as e:
        log_and_print(f"❌ Error running tool '{tool_name}': {e}")
        raise

