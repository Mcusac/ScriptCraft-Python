"""
Tool metadata discovery from impl tool packages.
"""

import importlib
import inspect
import pkgutil

from types import ModuleType
from typing import Dict, List, Optional

from scriptcraft._version import __version__

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    DEFAULT_TOOL_DISCOVERY_PATH,
    DEFAULT_TOOL_MODULE_PREFIX,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import ToolMetadata

_IMPL_TOOL_MODULE_PREFIX = DEFAULT_TOOL_MODULE_PREFIX
_IMPL_LEVEL_0_DIR = DEFAULT_TOOL_DISCOVERY_PATH


def _impl_tool_module(tool_name: str) -> str:
    return f"{_IMPL_TOOL_MODULE_PREFIX}.{tool_name}"


def _description_from_module(module: ModuleType, tool_name: str) -> str:
    for attr in dir(module):
        if attr.startswith("_"):
            continue
        obj = getattr(module, attr)
        if not inspect.isclass(obj):
            continue
        try:
            instance = obj()
        except Exception:
            continue
        description = getattr(instance, "description", None)
        if description:
            return str(description)
        doc = (obj.__doc__ or "").strip()
        if doc:
            return doc
    return f"🔧 {tool_name.replace('_', ' ').title()}"


def discover_tool_metadata(tool_name: str) -> Optional[ToolMetadata]:
    """Discover metadata for a tool package under the default impl tool root."""
    try:
        module = importlib.import_module(_impl_tool_module(tool_name))
    except ImportError:
        return None

    description = getattr(module, "__description__", None)
    if not description:
        description = _description_from_module(module, tool_name)

    return ToolMetadata(
        name=tool_name,
        version=getattr(module, "__version__", __version__),
        description=description,
        category=getattr(module, "__category__", "uncategorized"),
        tags=list(getattr(module, "__tags__", [])),
        data_types=list(getattr(module, "__data_types__", [])),
        domains=list(getattr(module, "__domains__", [])),
        complexity=getattr(module, "__complexity__", "simple"),
        maturity=getattr(module, "__maturity__", "stable"),
        distribution=getattr(module, "__distribution__", "hybrid"),
    )


def discover_all_tool_metadata() -> Dict[str, ToolMetadata]:
    """Scan default impl tool packages for tool metadata."""
    tools_metadata: Dict[str, ToolMetadata] = {}

    if not _IMPL_LEVEL_0_DIR.exists():
        return tools_metadata

    for _, name, is_pkg in pkgutil.iter_modules([str(_IMPL_LEVEL_0_DIR)]):
        if is_pkg and not name.startswith("_"):
            metadata = discover_tool_metadata(name)
            if metadata:
                tools_metadata[name] = metadata

    return tools_metadata


def get_tools_by_category() -> Dict[str, List[str]]:
    """Group tools by tag (category)."""
    all_metadata = discover_all_tool_metadata()
    categories: Dict[str, List[str]] = {}

    for tool_name, metadata in all_metadata.items():
        labels = metadata.tags or [metadata.category]
        for label in labels:
            if label:
                categories.setdefault(label, []).append(tool_name)

    return categories


def get_tools_by_maturity(maturity: str) -> List[str]:
    all_metadata = discover_all_tool_metadata()
    return [
        tool_name
        for tool_name, metadata in all_metadata.items()
        if metadata.maturity == maturity
    ]


def get_distributable_tools() -> List[str]:
    all_metadata = discover_all_tool_metadata()
    return [
        tool_name
        for tool_name, metadata in all_metadata.items()
        if metadata.distribution in ("standalone", "hybrid")
    ]


def update_tool_metadata(tool_name: str, **updates) -> bool:
    metadata = discover_tool_metadata(tool_name)
    if not metadata:
        return False

    suggestions = []
    for key, value in updates.items():
        attr_name = f"__{key}__"
        current_value = getattr(metadata, key, None)
        if current_value != value:
            if isinstance(value, list):
                suggestions.append(f"{attr_name} = {value}")
            else:
                suggestions.append(f'{attr_name} = "{value}"')

    return len(suggestions) > 0


def generate_metadata_summary() -> str:
    all_metadata = discover_all_tool_metadata()

    lines = ["# Tool Metadata Summary\n"]

    for tool_name, metadata in sorted(all_metadata.items()):
        lines.append(f"## {metadata.name}")
        lines.append(f"- **Version**: {metadata.version}")
        lines.append(f"- **Description**: {metadata.description}")
        lines.append(f"- **Complexity**: {metadata.complexity}")
        lines.append(f"- **Maturity**: {metadata.maturity}")
        lines.append(f"- **Distribution**: {metadata.distribution}")
        if metadata.tags:
            lines.append(f"- **Tags**: {', '.join(metadata.tags)}")
        if metadata.data_types:
            lines.append(f"- **Data Types**: {', '.join(metadata.data_types)}")
        if metadata.domains:
            lines.append(f"- **Domains**: {', '.join(metadata.domains)}")
        lines.append("")

    return "\n".join(lines)
