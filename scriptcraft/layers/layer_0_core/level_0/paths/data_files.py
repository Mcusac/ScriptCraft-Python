"""Tabular file discovery, resolution, copy, and move."""

import shutil

from pathlib import Path
from typing import List, Optional, Sequence, Union

_DATA_EXTENSIONS: Sequence[str] = (".csv", ".xlsx", ".xls")


def find_first_data_file(
    directory: Union[str, Path],
    extensions: Sequence[str] = _DATA_EXTENSIONS,
) -> Optional[Path]:
    """Return the first data file in *directory* matching common tabular extensions."""
    root = Path(directory)
    if not root.is_dir():
        return None

    for extension in extensions:
        matches = sorted(root.glob(f"*{extension}"))
        if matches:
            return matches[0]

    return None


def find_matching_file(
    directory: Union[str, Path],
    pattern: str,
) -> Optional[Path]:
    """Return the first file in *directory* whose name matches *pattern*, or None."""
    files = list(Path(directory).glob(pattern))
    return files[0] if files else None


def find_latest_file(
    directory: Union[str, Path],
    pattern: str = "*.csv",
) -> Optional[Path]:
    """Return the most recently modified file matching *pattern*, or None."""
    files = list(Path(directory).glob(pattern))
    return max(files, key=lambda f: f.stat().st_mtime) if files else None


def resolve_file(
    file_path: Union[str, Path],
    search_dirs: List[Union[str, Path]],
) -> Optional[Path]:
    """Locate *file_path* by searching each directory in *search_dirs*."""
    file_path = Path(file_path)
    if file_path.is_absolute() and file_path.exists():
        return file_path

    for directory in search_dirs:
        candidate = Path(directory) / file_path
        if candidate.exists():
            return candidate

    return None


def make_absolute(
    path: Union[str, Path],
    base_dir: Union[str, Path],
) -> Path:
    """Return *path* as an absolute path, resolved relative to *base_dir*."""
    path = Path(path)
    if path.is_absolute():
        return path
    return Path(base_dir) / path


def copy_file(
    source: Union[str, Path],
    destination: Union[str, Path],
    overwrite: bool = False,
) -> None:
    """Copy *source* to *destination*."""
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {destination}")

    shutil.copy2(source, destination)


def move_file(
    source: Union[str, Path],
    destination: Union[str, Path],
    overwrite: bool = False,
) -> None:
    """Move *source* to *destination*."""
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {destination}")

    shutil.move(str(source), str(destination))
