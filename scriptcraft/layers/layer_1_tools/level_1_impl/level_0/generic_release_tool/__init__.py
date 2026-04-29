"""
Generic Release Tool package.

This package contains a workspace-agnostic release tool that can be executed
directly (via its CLI) or imported as a tool class.
"""

from .cli import main
from .tool import GenericReleaseTool

__all__ = [
    "GenericReleaseTool",
    "main",
]

