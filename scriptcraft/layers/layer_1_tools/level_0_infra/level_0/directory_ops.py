"""
Low-level directory operations: creation, listing, and cleanup.

NOTE: The project-convention helpers at the bottom of this file
(get_input_dir, get_output_dir, get_qc_output_dir) encode hardcoded
layout assumptions and should be migrated to a higher-level path-convention
module when that refactor is possible.
"""

import shutil
from pathlib import Path
from typing import List, Optional, Union


# ── Generic directory operations ────────────────────────────────────────────

def ensure_output_dir(directory: Union[str, Path]) -> Path:
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
        pattern:   Glob pattern (default ``"*"``).
        recursive: If True, search subdirectories recursively.

    Returns:
        List of matching file Paths.
    """
    directory = Path(directory)
    return list(directory.rglob(pattern) if recursive else directory.glob(pattern))


# ── Project-convention helpers (legacy; encode hardcoded layout) ─────────────
# These functions know about the "input / output / qc_output / <domain>"
# directory layout.  They should live in a higher-level path-convention
# module; they are kept here only for backward compatibility.

def get_input_dir(domain: str) -> Path:
    """Return ``input/<domain>``."""
    return Path("input") / domain


def get_output_dir(domain: str) -> Path:
    """Return ``output/<domain>``."""
    return Path("output") / domain


def get_qc_output_dir(domain: str) -> Path:
    """Return ``qc_output/<domain>``."""
    return Path("qc_output") / domain


def get_file_output_path(
    domain: str,
    filename: str,
    subdir: Optional[str] = None,
) -> Path:
    """
    Compute the full output path for *filename* in the given domain.

    Side effect: creates the output directory if it does not exist.

    Args:
        domain:   Domain name.
        filename: Target filename.
        subdir:   Optional subdirectory under the domain output dir.

    Returns:
        Full Path to the intended output file.
    """
    output_dir = get_output_dir(domain)
    if subdir:
        output_dir = output_dir / subdir
    ensure_output_dir(output_dir)
    return output_dir / filename