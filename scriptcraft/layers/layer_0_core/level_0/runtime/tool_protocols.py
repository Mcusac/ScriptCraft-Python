"""Composable runtime contracts for lifecycle-driven tools."""

from pathlib import Path
from typing import Any, Optional, Protocol, Sequence, Union

PathLike = Union[str, Path]
InputPath = PathLike
InputPaths = list[InputPath]


class ToolLifecycle(Protocol):
    def log_start(self) -> None: ...

    def log_completion(self, *args: Any, **kwargs: Any) -> None: ...

    def log_error(self, e: Exception) -> None: ...


class InputValidation(Protocol):
    def validate_input_files(
        self,
        input_paths: Sequence[PathLike],
        required_count: int = 0,
    ) -> bool: ...


class OutputResolver(Protocol):
    def resolve_output_directory(self, output_dir: Optional[PathLike]) -> Path: ...


class DomainProcessor(Protocol):
    def process_domain(
        self,
        domain: str,
        dataset_file: Path,
        dictionary_file: Optional[PathLike],
        output_path: Path,
        **kwargs: Any,
    ) -> None: ...


class ProcessDomainTool(
    ToolLifecycle,
    InputValidation,
    OutputResolver,
    DomainProcessor,
    Protocol,
):
    """Tool contract for domain-over-input-path loops."""
    pass


class DomainLoopTool(
    ToolLifecycle,
    OutputResolver,
    Protocol,
):
    """Lighter contract for domain iteration loops."""
    pass
