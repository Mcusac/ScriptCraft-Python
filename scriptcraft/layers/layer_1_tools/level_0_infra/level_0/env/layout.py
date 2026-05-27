"""Dev vs distributable path resolution helpers."""

from pathlib import Path


def dev_project_root_from_file(file_path: Path, *, levels_up: int = 5) -> Path:
    """Walk up from ``file_path`` to the configured dev project root anchor."""
    current = Path(file_path).resolve().parent
    for _ in range(levels_up):
        current = current.parent
    return current


def get_environment_type_from_bool(is_distributable: bool) -> str:
    return "production" if is_distributable else "development"


def resolve_distributable_base_dir(*, cwd: Path | None = None) -> Path:
    return (cwd or Path.cwd()).resolve()
