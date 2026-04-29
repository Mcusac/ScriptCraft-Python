"""
ScriptCraft package root.

This repository is being consolidated into a layered architecture under
`scriptcraft.layers.*`. Import from the appropriate layer package(s) rather than
relying on legacy flat module paths.
"""

from ._version import __author__, __version__

# Expose the layered namespace as the primary surface area.
from . import layers  # noqa: F401

__all__ = [
    "__author__",
    "__version__",
    "layers",
]

