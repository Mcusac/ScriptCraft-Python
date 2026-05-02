"""
Canonical tool execution dispatcher.

This is the SINGLE SOURCE OF TRUTH for tool method resolution order:
check → validate → transform → run
"""

from typing import Any
from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print


def dispatch_tool(
    tool: Any,
    domain: str,
    input_path: str,
    output_path: str,
    paths: dict,
    **kwargs: Any
) -> None:
    """
    Unified execution policy for all tools.
    """

    try:
        log_and_print(f"🚀 Starting {tool.name} for {domain}")
        log_and_print(f"📂 Input: {input_path}")
        log_and_print(f"📂 Output: {output_path}")

        if hasattr(tool, "check"):
            return tool.check(domain, input_path, output_path, paths, **kwargs)

        if hasattr(tool, "validate"):
            return tool.validate(domain, input_path, output_path, paths, **kwargs)

        if hasattr(tool, "transform"):
            return tool.transform(domain, input_path, output_path, paths, **kwargs)

        if hasattr(tool, "run"):
            return tool.run(
                domain=domain,
                input_path=input_path,
                output_path=output_path,
                paths=paths,
                **kwargs,
            )

        raise AttributeError(
            f"{tool.__class__.__name__} has no recognized execution method"
        )

    except Exception as e:
        log_and_print(f"❌ Error in {tool.__class__.__name__} for {domain}: {e}")
        raise