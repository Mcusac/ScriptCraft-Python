
from dataclasses import dataclass
from typing import Any, Dict, Sequence


@dataclass(frozen=True)
class ParsedCli:
    mode: str
    kwargs: Dict[str, Any]


def parse_release_manager_argv(argv: Sequence[str]) -> ParsedCli:
    """
    Preserve the existing `release_manager_main.py` argv semantics:
    - argv[0] is the mode
    - remaining tokens: `--flag value` / `--flag` (bool) / positional values -> input_paths
    """
    if not argv:
        raise ValueError("argv is empty")

    mode = str(argv[0]).lower()
    remaining_args = list(argv[1:])

    kwargs: Dict[str, Any] = {}
    i = 0
    while i < len(remaining_args):
        arg = remaining_args[i]
        if isinstance(arg, str) and arg.startswith("--"):
            key = arg[2:].replace("-", "_")
            if i + 1 < len(remaining_args) and not str(remaining_args[i + 1]).startswith("--"):
                kwargs[key] = remaining_args[i + 1]
                i += 2
            else:
                kwargs[key] = True
                i += 1
        else:
            kwargs.setdefault("input_paths", [])
            kwargs["input_paths"].append(arg)
            i += 1

    kwargs["mode"] = mode

    # Preserve the old post-processing behavior (minimal type coercion).
    if "version_type" in kwargs:
        kwargs["version_type"] = str(kwargs["version_type"])
    if "auto_push" in kwargs:
        kwargs["auto_push"] = True
    if "force" in kwargs:
        kwargs["force"] = True
    if "skip_pypi" in kwargs:
        kwargs["skip_pypi"] = True

    return ParsedCli(mode=mode, kwargs=kwargs)

