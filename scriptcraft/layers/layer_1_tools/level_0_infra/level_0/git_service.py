"""
GitService

Single source of truth for all Git operations.

Design goals:
- No subprocess calls outside this service
- No duplicated git logic across tools
- Consistent cwd handling
- Minimal, testable surface area
- Clear separation between queries (read) and commands (write)
"""
import subprocess

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List


@dataclass(frozen=True)
class GitResult:
    returncode: int
    stdout: str
    stderr: str


class GitService:
    """
    Centralized Git interface.

    All tools must depend on this instead of calling subprocess or probes directly.
    """

    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or Path.cwd()

    # ---------------------------------------------------------------------
    # Core runner
    # ---------------------------------------------------------------------

    def _run(self, args: List[str]) -> GitResult:
        result = subprocess.run(
            args,
            cwd=str(self.repo_root),
            capture_output=True,
            text=True,
        )

        return GitResult(
            returncode=result.returncode,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
        )

    def _run_git(self, command: str) -> GitResult:
        return self._run(["git"] + command.split())

    # ---------------------------------------------------------------------
    # Repository state
    # ---------------------------------------------------------------------

    def is_repo(self) -> bool:
        """Check if directory is a git repository."""
        return (self.repo_root / ".git").exists()

    def status_porcelain(self) -> str:
        """Raw porcelain status output."""
        result = self._run_git("status --porcelain")
        return result.stdout.strip()

    def is_clean(self) -> bool:
        """True if working tree has no changes."""
        return self.status_porcelain() == ""

    def has_changes(self) -> bool:
        """True if working tree has uncommitted changes."""
        return not self.is_clean()

    def has_submodules(self) -> bool:
        """True if repo contains submodules."""
        result = self._run_git("submodule status")
        return bool(result.stdout.strip())

    # ---------------------------------------------------------------------
    # Basic workflows
    # ---------------------------------------------------------------------

    def add_all(self) -> bool:
        result = self._run_git("add .")
        return result.returncode == 0

    def commit(self, message: str) -> bool:
        result = self._run(["git", "commit", "-m", message])
        return result.returncode == 0

    def push(self) -> bool:
        result = self._run_git("push")
        return result.returncode == 0

    def push_tags(self) -> bool:
        result = self._run_git("push --tags")
        return result.returncode == 0

    def pull(self) -> bool:
        result = self._run_git("pull")
        return result.returncode == 0

    # ---------------------------------------------------------------------
    # Tagging
    # ---------------------------------------------------------------------

    def create_tag(self, version: str) -> bool:
        result = self._run(["git", "tag", f"v{version}"])
        return result.returncode == 0

    # ---------------------------------------------------------------------
    # Composite operations (optional convenience layer)
    # ---------------------------------------------------------------------

    def commit_all(self, message: str) -> bool:
        if not self.add_all():
            return False
        return self.commit(message)

    def push_full(self) -> bool:
        if not self.push():
            return False
        return self.push_tags()