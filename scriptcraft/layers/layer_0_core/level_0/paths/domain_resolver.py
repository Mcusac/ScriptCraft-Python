"""Abstract path resolution and standard domain directory layout."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict


class PathResolver(ABC):
    """Abstract interface for workspace-aware path resolution."""

    @abstractmethod
    def get_workspace_root(self) -> Path: ...

    @abstractmethod
    def get_input_dir(self) -> Path: ...

    @abstractmethod
    def get_output_dir(self) -> Path: ...

    @abstractmethod
    def get_logs_dir(self) -> Path: ...

    @abstractmethod
    def get_domains_dir(self) -> Path: ...

    @abstractmethod
    def get_qc_output_dir(self) -> Path: ...

    @abstractmethod
    def get_domain_paths(self, domain: str) -> Dict[str, Path]: ...


def build_domain_paths(domain_base: Path) -> Dict[str, Path]:
    """
    Return the standard subdirectory layout for a single domain.

    This is the single source of truth for domain directory keys across
    the entire project.
    """
    return {
        "root": domain_base,
        "raw_data": domain_base / "raw_data",
        "processed_data": domain_base / "processed_data",
        "merged_data": domain_base / "merged_data",
        "old_data": domain_base / "old_data",
        "dictionary": domain_base / "dictionary",
        "qc_output": domain_base / "qc_output",
        "qc_logs": domain_base / "qc_logs",
    }
