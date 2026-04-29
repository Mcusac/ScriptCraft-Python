"""
Argparse-namespace to tool.run(**kwargs) mapping.

This keeps CLI-arg shape decisions separate from dispatch/execution and from tool
implementations.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def _normalize_input_paths(args: Any) -> Optional[List[Union[str, Path]]]:
    if not hasattr(args, "input"):
        return None

    value = getattr(args, "input")
    if value is None:
        return None

    if isinstance(value, (str, Path)):
        return [value]

    # Best-effort: treat as an iterable of path-likes
    try:
        return list(value)
    except TypeError:
        return [value]


def build_run_kwargs_from_args(args: Any) -> Dict[str, Any]:
    """
    Map known standard CLI args to `BaseTool.run(...)` kwargs.

    This intentionally preserves the legacy mapping used by the old dispatcher.
    """
    return {
        "mode": getattr(args, "mode", None),
        "input_paths": _normalize_input_paths(args),
        "output_dir": getattr(args, "output", "output"),
        "domain": getattr(args, "domain", None),
        "output_filename": getattr(args, "output_filename", None),
    }

