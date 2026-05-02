from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from layers.layer_1_tools.level_0_infra.level_0.version import __version__
from layers.layer_1_tools.level_0_infra.level_0.core_types import ComponentType


@dataclass
class ToolMetadata:
    name: str
    version: str = __version__
    description: str = ""
    category: str = "uncategorized"
    tags: List[str] = field(default_factory=list)
    data_types: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    complexity: str = "simple"
    maturity: str = "stable"
    distribution: str = "hybrid"
    dependencies: List[str] = field(default_factory=list)
    author: str = ""
    maintainer: str = ""


@dataclass
class PluginMetadata:
    name: str
    plugin_type: str
    description: str = ""
    version: str = __version__
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComponentMetadata:
    name: str
    type: ComponentType
    description: str
    tags: List[str] = field(default_factory=list)
    version: str = __version__
    author: str = "ScriptCraft Team"
    entry_point: Optional[str] = None
    config_schema: Optional[Dict[str, Any]] = None
    dependencies: List[str] = field(default_factory=list)
    is_experimental: bool = False
    is_deprecated: bool = False