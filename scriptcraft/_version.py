"""
Package root version shim.

`scriptcraft.layers.layer_1_tools.level_0_infra.level_0.version` remains the single source of
truth; this module exists to support conventional `scriptcraft.__version__`
imports.
"""

from layers.layer_1_tools.level_0_infra.level_0.version import (  # noqa: F401
    __author__,
    __version__,
    get_version,
    get_version_info,
)

__all__ = [
    "__author__",
    "__version__",
    "get_version",
    "get_version_info",
]

