"""
Explicit contracts for runtime helper functions (SOLID/ISP).
"""

from pathlib import Path
from typing import Any, Optional, Protocol, Sequence, Union

PathLike = Union[str, Path]


class ProcessDomainTool(Protocol):
    def log_start(self) -> None: ...

    def log_completion(self) -> None: ...

    def log_error(self, e: Exception) -> None: ...

    def validate_input_files(self, input_paths: Sequence[PathLike]) -> bool: ...

    def resolve_output_directory(self, output_dir: Optional[PathLike]) -> Path: ...

    def process_domain(
        self,
        domain: str,
        dataset_file: Path,
        dictionary_file: Optional[PathLike],
        output_path: Path,
        **kwargs: Any,
    ) -> None: ...


class DomainLoopTool(Protocol):
    def log_start(self) -> None: ...

    def log_completion(self) -> None: ...

    def log_error(self, e: Exception) -> None: ...

    def resolve_output_directory(self, output_dir: Optional[PathLike]) -> Path: ...

