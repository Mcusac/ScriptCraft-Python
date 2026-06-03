"""
Shared impl tool discovery roots.

Single source for filesystem scan paths and import prefixes used by metadata
discovery (level_2) and runtime discovery wiring (level_1+).
"""

from pathlib import Path

_LAYER_1_TOOLS_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_TOOL_DISCOVERY_PATH = _LAYER_1_TOOLS_ROOT / "level_1_impl" / "level_0"

DEFAULT_TOOL_MODULE_PREFIX = (
    "scriptcraft.layers.layer_1_tools.level_1_impl.level_0"
)


def default_tool_discovery_paths() -> list[Path]:
    """Return default on-disk tool package roots for discovery."""
    return [DEFAULT_TOOL_DISCOVERY_PATH]
