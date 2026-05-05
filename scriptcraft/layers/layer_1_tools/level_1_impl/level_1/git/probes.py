"""
Git probe helpers.

These are read-only probes used by git-related tools.

NOTE:
This module is now a thin compatibility layer over GitService.
It preserves existing function signatures so no downstream code breaks,
but delegates all logic to the canonical GitService implementation.
"""

from pathlib import Path
from typing import Optional

from layers.layer_1_tools.level_1_impl.level_0.git_service import GitService


# ---------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------

def _get_service(cwd: Optional[Path]) -> GitService:
    """
    Create a GitService instance for the given cwd.
    Falls back to current working directory if None.
    """
    return GitService(repo_root=cwd or Path("."))


# ---------------------------------------------------------------------
# Public probes (backward compatible API)
# ---------------------------------------------------------------------

def is_git_repo(repo_root: Path = Path(".")) -> bool:
    """
    Return True if `repo_root` looks like a git repository root.

    Kept identical behavior (no subprocess dependency).
    """
    return (repo_root / ".git").exists()


def porcelain_status_has_changes(*, cwd: Optional[Path] = None) -> bool:
    """
    Return True if `git status --porcelain` indicates modifications.

    Delegates to GitService to ensure single source of truth.
    """
    git = _get_service(cwd)
    return git.has_changes()


def has_submodules(*, cwd: Optional[Path] = None) -> bool:
    """
    Return True if `git submodule status` outputs any rows.

    Delegates to GitService for consistency.
    """
    git = _get_service(cwd)
    return git.has_submodules()