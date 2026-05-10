from pathlib import Path
from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.path_resolver import WorkspacePathResolver
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.workspace_schema import WorkspaceConfig
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1.framework_schema import FrameworkConfig
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.root_schema import Config


def load_legacy_config(data: Dict[str, Any], path: Path) -> "Config":
    """
    Load legacy configuration (backward compatibility).

    Supports two legacy shapes:
    - "framework-like" legacy config containing active_workspace/workspaces/packaging/paths
    - "workspace-like" legacy config containing workspace fields at the root
    """
    if "active_workspace" in data:
        framework = FrameworkConfig(
            active_workspace=data.get("active_workspace", "data"),
            workspace_base_path=data.get("workspace_base_path", "."),
            available_workspaces=data.get("workspaces", ["data"]),
            packaging=data.get("packaging", {}),
            paths=data.get("paths", {}),
        )

        workspace = WorkspaceConfig()
        config = Config(
            framework=framework,
            workspace=workspace,
            tools=data.get("tools", {}),
            pipelines=data.get("pipelines", {}),
            tool_configs=data.get("tool_configs", {}),
        )
    else:
        framework = FrameworkConfig()
        workspace = WorkspaceConfig(**data)
        config = Config(
            framework=framework,
            workspace=workspace,
            tools=data.get("tools", {}),
            pipelines=data.get("pipelines", {}),
            tool_configs=data.get("tool_configs", {}),
        )

    config.workspace_root = path.parent.resolve()
    config._path_resolver = WorkspacePathResolver(config.workspace_root)
    return config

