"""
Git workspace tool package.

Public API:
- GitWorkspaceTool: programmatic entrypoint
- main: CLI entrypoint (raises SystemExit)
"""

from .cli import main
from .tool import GitWorkspaceTool

__all__ = [
    "GitWorkspaceTool",
    "main",
]

