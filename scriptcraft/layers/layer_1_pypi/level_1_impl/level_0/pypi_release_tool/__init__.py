"""
PyPI Release Tool (package)

This package contains a focused, DRY implementation of the PyPI release tool:
- CLI parsing (`cli.py`)
- Tool orchestration (`tool.py`)
- Focused operations (`ops_*`)
"""

from .tool import PyPIReleaseTool
from .cli import main

__all__ = ["PyPIReleaseTool", "main"]

