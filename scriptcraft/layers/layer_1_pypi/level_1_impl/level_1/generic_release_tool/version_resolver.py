"""
Repo-first version resolution for the Generic Release Tool.

This avoids importing `scriptcraft` directly, which may resolve to an installed
package rather than the repository being released.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from importlib import metadata

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_pypi.level_1_impl.level_0.versioning.version_file import (
    get_current_version,
    get_pyproject_version,
)


@dataclass(frozen=True)
class VersionResolution:
    version: str
    source: str
    repo_root: Optional[Path]


def detect_repo_root(*, start: Path) -> Optional[Path]:
    """
    Walk upward from `start` looking for release-relevant repo markers.

    Markers:
    - `pyproject.toml`
    - `scriptcraft/_version.py`
    """
    cursor = start.resolve()
    if cursor.is_file():
        cursor = cursor.parent

    for parent in [cursor, *cursor.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
        if (parent / "scriptcraft" / "_version.py").exists():
            return parent
    return None


def resolve_version(*, repo_root: Optional[Path]) -> VersionResolution:
    """
    Resolve version with repo-first precedence.

    Order:
    1) `pyproject.toml` ([project].version)
    2) `scriptcraft/_version.py`
    3) Installed distribution metadata (best-effort)
    """
    if repo_root is not None:
        pyproject_file = repo_root / "pyproject.toml"
        if pyproject_file.exists():
            v = get_pyproject_version(pyproject_file=pyproject_file)
            if v:
                return VersionResolution(version=v, source="pyproject.toml:[project].version", repo_root=repo_root)

        version_file = repo_root / "scriptcraft" / "_version.py"
        if version_file.exists():
            v = get_current_version(version_file=version_file)
            if v:
                return VersionResolution(version=v, source="scriptcraft/_version.py", repo_root=repo_root)

    # Fallback: installed package metadata.
    try:
        v = metadata.version("scriptcraft-python")
        return VersionResolution(version=v, source="importlib.metadata:scriptcraft-python", repo_root=repo_root)
    except Exception:
        pass

    try:
        v = metadata.version("scriptcraft")
        return VersionResolution(version=v, source="importlib.metadata:scriptcraft", repo_root=repo_root)
    except Exception:
        log_and_print("⚠️ Could not resolve version; defaulting to 0.0.0", level="warning")
        return VersionResolution(version="0.0.0", source="default", repo_root=repo_root)

