"""
Release manager tool package.

Public API:
- ReleaseManager: programmatic entrypoint
- main: CLI entrypoint (exit code as int)
"""

from .cli import main
from .tool import ReleaseManager

__all__ = [
    "ReleaseManager",
    "main",
]

