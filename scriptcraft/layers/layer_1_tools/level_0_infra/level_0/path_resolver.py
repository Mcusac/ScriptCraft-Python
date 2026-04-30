"""
Path resolution: abstract base and two concrete workspace resolvers.

Callers are responsible for creating directories; resolvers only compute paths.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Optional


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
    the entire project. Any code that constructs domain path dicts should
    call this function rather than building the dict inline.
    """
    return {
        "root":           domain_base,
        "raw_data":       domain_base / "raw_data",
        "processed_data": domain_base / "processed_data",
        "merged_data":    domain_base / "merged_data",
        "old_data":       domain_base / "old_data",
        "dictionary":     domain_base / "dictionary",
        "qc_output":      domain_base / "qc_output",
        "qc_logs":        domain_base / "qc_logs",
    }


class WorkspacePathResolver(PathResolver):
    """
    Path resolver for the multi-workspace project layout.

    Does NOT create directories on construction. Call
    ``ensure_workspace_dirs()`` explicitly when directory creation is needed.
    """

    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = Path(workspace_root).resolve()

    def ensure_workspace_dirs(self) -> None:
        """Create the standard top-level workspace directories if absent."""
        for name in ("input", "output", "logs"):
            (self.workspace_root / name).mkdir(parents=True, exist_ok=True)

    def get_workspace_root(self) -> Path:
        return self.workspace_root

    def get_input_dir(self) -> Path:
        return self.workspace_root / "input"

    def get_output_dir(self) -> Path:
        return self.workspace_root / "output"

    def get_logs_dir(self) -> Path:
        return self.workspace_root / "logs"

    def get_domains_dir(self) -> Path:
        return self.workspace_root / "domains"

    def get_qc_output_dir(self) -> Path:
        return self.workspace_root / "qc_output"

    def get_domain_paths(self, domain: str) -> Dict[str, Path]:
        return build_domain_paths(self.get_domains_dir() / domain)

    def get_all_domain_paths(self) -> Dict[str, Dict[str, Path]]:
        """Return path dicts for every domain directory that exists."""
        domains_dir = self.get_domains_dir()
        if not domains_dir.exists():
            return {}
        return {
            d.name: self.get_domain_paths(d.name)
            for d in domains_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        }

    def resolve_input_path(
        self, input_key: str, domain: Optional[str] = None
    ) -> Optional[Path]:
        """Resolve an input path from a key, with optional domain scoping."""
        global_inputs: Dict[str, Path] = {
            "rhq_inputs":  self.get_input_dir(),
            "global_data": self.get_input_dir(),
        }
        if input_key in global_inputs:
            return global_inputs[input_key]
        if domain:
            return self.get_domain_paths(domain).get(input_key)
        return None

    def resolve_output_path(
        self,
        output_filename: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> Path:
        """Resolve an output path, optionally scoped to a domain."""
        base = (
            self.get_domain_paths(domain)["qc_output"]
            if domain
            else self.get_output_dir()
        )
        return base / output_filename if output_filename else base


class LegacyPathResolver(PathResolver):
    """Path resolver for the flat (legacy) project layout."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = Path(project_root).resolve()

    def get_workspace_root(self) -> Path:
        return self.project_root

    def get_input_dir(self) -> Path:
        return self.project_root / "input"

    def get_output_dir(self) -> Path:
        return self.project_root / "output"

    def get_logs_dir(self) -> Path:
        return self.project_root / "logs"

    def get_domains_dir(self) -> Path:
        return self.project_root / "domains"

    def get_qc_output_dir(self) -> Path:
        return self.project_root / "qc_output"

    def get_domain_paths(self, domain: str) -> Dict[str, Path]:
        return build_domain_paths(self.get_domains_dir() / domain)


def create_path_resolver(
    workspace_root: Path,
    *,
    legacy: bool = False,
) -> PathResolver:
    """
    Factory: return a resolver for the given root.

    Args:
        workspace_root: Explicit root directory.
        legacy:         If True, return a ``LegacyPathResolver``.
    """
    if legacy:
        return LegacyPathResolver(workspace_root)
    return WorkspacePathResolver(workspace_root)