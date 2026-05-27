"""Generic guarded lifecycle runner for tools and workflows."""

from pathlib import Path
from typing import Any, Callable, Optional, Sequence, Union

from scriptcraft.layers.layer_0_core.level_0 import PathLike, ToolLifecycle


def run_guarded_lifecycle(
    subject: ToolLifecycle,
    *,
    work: Callable[[], None],
    output_dir: Optional[Union[str, Path]] = None,
) -> None:
    """Standard log_start / work / log_completion with error propagation."""
    subject.log_start()
    try:
        work()
        if output_dir is not None and hasattr(subject, "resolve_output_directory"):
            subject.log_completion(subject.resolve_output_directory(output_dir))  # type: ignore[attr-defined]
        else:
            subject.log_completion()
    except Exception as exc:
        subject.log_error(exc)
        raise


def run_with_validated_inputs(
    subject: Any,
    *,
    input_paths: Optional[Sequence[PathLike]],
    required_count: Optional[int] = None,
    output_dir: Optional[Union[str, Path]] = None,
    work: Callable[[Path], None],
) -> None:
    """Validate inputs, resolve output directory, then run per-input work."""

    def _execute() -> None:
        paths = list(input_paths or [])
        if required_count is not None and len(paths) < required_count:
            raise ValueError(f"Need at least {required_count} input file(s)")
        if paths and not subject.validate_input_files(
            paths,
            required_count=required_count or 0,
        ):
            raise ValueError("Invalid input files")
        output_path = subject.resolve_output_directory(
            output_dir or subject.default_output_dir,
        )
        for input_path in paths:
            work(output_path, Path(input_path))

    run_guarded_lifecycle(subject, work=_execute, output_dir=output_dir)
