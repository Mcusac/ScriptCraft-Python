"""
Git probe helpers.

These are read-only probes used by git-related tools.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from layers.layer_1_tools.level_1_impl.level_0.subprocess.runner import _run


def is_git_repo(repo_root: Path = Path(".")) -> bool:
    """Return True if `repo_root` looks like a git repository root."""
    return (repo_root / ".git").exists()


def porcelain_status_has_changes(*, cwd: Optional[Path] = None) -> bool:
    """Return True if `git status --porcelain` indicates modifications."""
    result = _run("git status --porcelain", cwd=cwd, check=False)
    return bool(result.stdout.strip())


def has_submodules(*, cwd: Optional[Path] = None) -> bool:
    """Return True if `git submodule status` outputs any rows."""
    result = _run("git submodule status", cwd=cwd, check=False)
    return bool(result.stdout.strip())

