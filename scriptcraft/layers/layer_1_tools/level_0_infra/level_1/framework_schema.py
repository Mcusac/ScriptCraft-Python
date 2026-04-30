from dataclasses import dataclass, field
from typing import Any, Dict, List

from layers.layer_1_tools.level_0_infra.level_0.version import get_version


@dataclass
class FrameworkConfig:
    version: str = field(default_factory=get_version)
    active_workspace: str = "data"
    workspace_base_path: str = "."
    available_workspaces: List[str] = field(default_factory=lambda: ["data"])
    packaging: Dict[str, Any] = field(default_factory=dict)
    paths: Dict[str, Any] = field(default_factory=dict)