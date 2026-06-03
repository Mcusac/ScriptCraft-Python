"""
Workspace path resolver built on core ``PathResolver`` abstractions.

Import ``PathResolver`` and ``build_domain_paths`` from
``scriptcraft.layers.layer_0_core.level_0.paths`` (not from this module).
"""

from pathlib import Path
from typing import Dict, Optional

from scriptcraft.layers.layer_0_core.level_0.paths import (
    PathResolver,
    build_domain_paths,
)


class WorkspacePathResolver(PathResolver):
    """
    Path resolver for the multi-workspace project layout.

    Does NOT create directories on construction.
    """

    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = Path(workspace_root).resolve()

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
        self,
        input_key: str,
        domain: Optional[str] = None,
    ) -> Optional[Path]:
        """
        Resolve an input path from a key.

        NOTE: This is light routing logic; avoid expanding this into a large rule system.
        """
        global_inputs: Dict[str, Path] = {
            "rhq_inputs": self.get_input_dir(),
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
