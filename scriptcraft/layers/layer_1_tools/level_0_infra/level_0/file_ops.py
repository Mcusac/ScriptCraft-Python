"""
Low-level file operations: discovery, resolution, copy, and move.
"""

import shutil
from pathlib import Path
from typing import List, Optional, Union


def find_matching_file(
    directory: Union[str, Path],
    pattern: str,
) -> Optional[Path]:
    """
    Return the first file in *directory* whose name matches *pattern*, or None.

    Args:
        directory: Directory to search.
        pattern:   Glob pattern (e.g. ``"*.csv"``).

    Returns:
        Path to the first match, or None if no file matches.
    """
    files = list(Path(directory).glob(pattern))
    return files[0] if files else None


def find_latest_file(
    directory: Union[str, Path],
    pattern: str = "*.csv",
) -> Optional[Path]:
    """
    Return the most recently modified file matching *pattern*, or None.

    Args:
        directory: Directory to search.
        pattern:   Glob pattern (default ``"*.csv"``).

    Returns:
        Path to the newest match, or None if no file matches.
    """
    files = list(Path(directory).glob(pattern))
    return max(files, key=lambda f: f.stat().st_mtime) if files else None


def resolve_file(
    file_path: Union[str, Path],
    search_dirs: List[Union[str, Path]],
) -> Optional[Path]:
    """
    Locate *file_path* by searching each directory in *search_dirs*.

    If *file_path* is absolute and exists it is returned immediately.

    Args:
        file_path:   Filename or relative path to find.
        search_dirs: Ordered list of directories to search.

    Returns:
        Resolved absolute Path, or None if not found.
    """
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
    """
    Return *path* as an absolute path, resolved relative to *base_dir*.

    Args:
        path:     Relative or absolute path.
        base_dir: Base directory used when *path* is relative.

    Returns:
        Absolute Path object.
    """
    path = Path(path)
    if path.is_absolute():
        return path
    return Path(base_dir) / path


def copy_file(
    source: Union[str, Path],
    destination: Union[str, Path],
    overwrite: bool = False,
) -> None:
    """
    Copy *source* to *destination*.

    Args:
        source:      Source file path.
        destination: Destination file path.
        overwrite:   If False (default), raise FileExistsError when destination exists.

    Raises:
        FileNotFoundError: Source does not exist.
        FileExistsError:   Destination exists and *overwrite* is False.
    """
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
    """
    Move *source* to *destination*.

    Args:
        source:      Source file path.
        destination: Destination file path.
        overwrite:   If False (default), raise FileExistsError when destination exists.

    Raises:
        FileNotFoundError: Source does not exist.
        FileExistsError:   Destination exists and *overwrite* is False.
    """
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {destination}")

    shutil.move(str(source), str(destination))