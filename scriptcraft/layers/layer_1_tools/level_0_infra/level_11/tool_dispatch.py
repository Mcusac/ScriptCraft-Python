"""
Tool dispatch execution by tool name.

Responsibilities:
- resolve a tool class by name (via ToolLookup)
- instantiate the tool
- map CLI args to `run()` kwargs
- execute with consistent error handling/logging
"""

import sys

from argparse import Namespace
from typing import Any, Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    build_run_kwargs_from_args,
    log_and_print,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_10.tool_lookup import (
    ToolLookup,
)


def dispatch_tool_by_name(
    tool_name: str,
    args: Any = None,
    *,
    lookup: Optional["ToolLookup"] = None,
    exit_on_failure: bool = True,
) -> bool:
    """Resolve and execute a tool class by name."""
    if lookup is None:
        from scriptcraft.layers.layer_1_tools.level_0_infra.level_10.tool_lookup import (
            InfraRegistryToolLookup,
        )

        effective_lookup = InfraRegistryToolLookup()
    else:
        effective_lookup = lookup

    effective_args = args if args is not None else Namespace()

    try:
        tool_class = effective_lookup.get_tool_class(tool_name)
        if tool_class is None:
            raise ValueError(f"Tool '{tool_name}' not found.")

        log_and_print(f"🚀 Running tool: {tool_name}")

        tool_instance = tool_class()
        run_kwargs = build_run_kwargs_from_args(effective_args)
        success = tool_instance.run(**run_kwargs)

        if success is False:
            log_and_print(f"❌ Tool '{tool_name}' failed", level="error")
            if exit_on_failure:
                sys.exit(1)
            return False

        log_and_print(f"✅ Tool '{tool_name}' completed successfully")
        return True

    except SystemExit:
        raise
    except Exception as e:
        log_and_print(
            f"❌ Error running tool '{tool_name}': {e}",
            level="error",
        )
        if exit_on_failure:
            sys.exit(1)
        raise

    return True
