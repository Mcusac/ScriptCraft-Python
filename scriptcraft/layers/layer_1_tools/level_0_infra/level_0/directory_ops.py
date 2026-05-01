"""
Low-level directory operations: creation, listing, and cleanup.

This module MUST remain layout-agnostic.
It should never encode project-specific directory structures.
"""

import shutil
from pathlib import Path
from typing import List, Union


def ensure_dir(directory: Union[str, Path]) -> Path:
    """
    Create *directory* (and parents) if it does not exist.

    Args:
        directory: Target directory path.

    Returns:
        The resolved directory Path.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def clean_directory(directory: Union[str, Path]) -> None:
    """
    Delete all contents of *directory* and re-create it as an empty directory.

    Args:
        directory: Directory to clean.
    """
    directory = Path(directory)

    if directory.exists():
        shutil.rmtree(directory)

    directory.mkdir(parents=True)


def list_files(
    directory: Union[str, Path],
    pattern: str = "*",
    recursive: bool = False,
) -> List[Path]:
    """
    Return all files in *directory* matching *pattern*.

    Args:
        directory: Directory to search.
        pattern:   Glob pattern (default "*").
        recursive: If True, search subdirectories recursively.

    Returns:
        List of matching file Paths.
    """
    directory = Path(directory)

    if recursive:
        return list(directory.rglob(pattern))

    return list(directory.glob(pattern))