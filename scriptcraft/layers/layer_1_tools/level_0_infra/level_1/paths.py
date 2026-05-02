"""
Filesystem and project path utilities.

Depends ONLY on config_loader (not raw globals).
"""

from pathlib import Path
from typing import Dict, Optional

from layers.layer_1_tools.level_0_infra.level_1.config_loader import get_config
from layers.layer_1_tools.level_0_infra.level_0.path_resolver import build_domain_paths


def get_project_root() -> Path:
    """
    Locate project root using structural markers.
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "config.yaml").exists() or (parent / "run_all.py").exists():
            return parent
    return Path(__file__).resolve().parents[2]


def get_domain_paths(project_root: Path) -> Dict[str, Dict[str, Path]]:
    domain_paths: Dict[str, Dict[str, Path]] = {}
    domains_dir = project_root / "domains"

    if not domains_dir.exists():
        return domain_paths

    for domain_dir in domains_dir.iterdir():
        if domain_dir.is_dir() and not domain_dir.name.startswith("."):
            domain_paths[domain_dir.name] = build_domain_paths(domain_dir)

    return domain_paths


def get_domain_output_path(
    domain_paths: Dict[str, Path],
    filename: Optional[str] = None,
    suffix: Optional[str] = None,
) -> Path:
    output_dir = domain_paths.get("qc_output", Path("output"))

    if filename:
        if suffix:
            stem, _, ext = filename.rpartition(".")
            filename = f"{stem}_{suffix}.{ext}" if stem else f"{filename}_{suffix}"
        return output_dir / filename

    return output_dir


def resolve_path(path: str | Path, base_dir: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else Path(base_dir) / p