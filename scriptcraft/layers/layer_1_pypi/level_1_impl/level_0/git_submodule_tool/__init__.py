"""
Git submodule tool package.

Public API:
- GitSubmoduleTool: programmatic entrypoint
- main: CLI entrypoint (exit code as int)
"""

from .cli import main
from .tool import GitSubmoduleTool

__all__ = [
    "GitSubmoduleTool",
    "main",
]

