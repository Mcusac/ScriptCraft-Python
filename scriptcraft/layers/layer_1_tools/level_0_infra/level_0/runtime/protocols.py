"""
Explicit contracts for runtime helper functions (SOLID/ISP compliant).

Key principles:
- Separate lifecycle concerns (logging, error handling)
- Separate IO/environment concerns (path resolution, validation)
- Keep domain processing focused and minimal
- Allow flexible composition of capabilities
"""

from pathlib import Path
from typing import Any, Optional, Protocol, Sequence, Union

PathLike = Union[str, Path]


# -----------------------------
# Lifecycle / Logging Concerns
# -----------------------------
class ToolLifecycle(Protocol):
    def log_start(self) -> None: ...

    def log_completion(self) -> None: ...

    def log_error(self, e: Exception) -> None: ...


# -----------------------------
# Input Validation
# -----------------------------
class InputValidation(Protocol):
    def validate_input_files(self, input_paths: Sequence[PathLike]) -> bool: ...


# -----------------------------
# Output Resolution
# -----------------------------
class OutputResolver(Protocol):
    def resolve_output_directory(self, output_dir: Optional[PathLike]) -> Path: ...


# -----------------------------
# Core Domain Processing
# -----------------------------
class DomainProcessor(Protocol):
    def process_domain(
        self,
        domain: str,
        dataset_file: Path,
        dictionary_file: Optional[PathLike],
        output_path: Path,
        **kwargs: Any,
    ) -> None: ...


# -----------------------------
# Composed Protocols (Use Cases)
# -----------------------------
class ProcessDomainTool(
    ToolLifecycle,
    InputValidation,
    OutputResolver,
    DomainProcessor,
    Protocol,
):
    """
    Full-featured tool used by run_process_domain_over_input_paths.
    This composes all required capabilities.
    """
    pass


class DomainLoopTool(
    ToolLifecycle,
    OutputResolver,
    Protocol,
):
    """
    Lighter-weight tool for looping operations.
    """
    pass