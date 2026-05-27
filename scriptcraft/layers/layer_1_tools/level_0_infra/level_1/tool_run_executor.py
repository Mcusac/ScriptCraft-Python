"""Shared BaseTool.run lifecycle helpers (infra adapter over core)."""
from pathlib import Path
from typing import Any, Callable, Optional, Sequence, Union

from scriptcraft.layers.layer_0_core.level_1.runtime.mode_execution import execute_mode, get_mode
from scriptcraft.layers.layer_0_core.level_0.runtime.tool_protocols import PathLike
from scriptcraft.layers.layer_0_core.level_1.runtime.tool_lifecycle import (
    run_guarded_lifecycle,
    run_with_validated_inputs as core_run_with_validated_inputs,
)


def run_tool_lifecycle(
    tool: Any,
    *,
    work: Callable[[], None],
    output_dir: Optional[Union[str, Path]] = None,
) -> None:
    """Standard log_start / work / log_completion with error propagation."""
    run_guarded_lifecycle(tool, work=work, output_dir=output_dir)


def run_with_validated_inputs(
    tool: Any,
    *,
    input_paths: Optional[Sequence[PathLike]],
    required_count: Optional[int] = None,
    output_dir: Optional[Union[str, Path]] = None,
    work: Callable[[Path], None],
) -> None:
    """Validate inputs, resolve output directory, then run per-input work."""
    core_run_with_validated_inputs(
        tool,
        input_paths=input_paths,
        required_count=required_count,
        output_dir=output_dir,
        work=work,
    )


def run_mode_dispatch(
    tool: Any,
    *,
    mode: Optional[str],
    registry: Any,
    input_paths: Optional[Sequence[PathLike]] = None,
    output_dir: Optional[Union[str, Path]] = None,
    domain: Optional[str] = None,
    default_mode: Optional[str] = None,
    **kwargs: Any,
) -> None:
    """Resolve mode from registry and execute via core mode runner."""
    resolved_mode = mode or default_mode
    if not resolved_mode:
        raise ValueError("mode is required")

    def _execute() -> None:
        output_path = tool.resolve_output_directory(output_dir or tool.default_output_dir)
        runner = get_mode(registry, resolved_mode)
        result = execute_mode(
            runner,
            mode=resolved_mode,
            input_paths=input_paths,
            output_dir=output_path,
            domain=domain,
            **kwargs,
        )
        if not getattr(result, "success", False):
            err = getattr(result, "error", None) or f"Mode '{resolved_mode}' failed"
            raise RuntimeError(str(err))

    run_tool_lifecycle(tool, work=_execute, output_dir=output_dir)
