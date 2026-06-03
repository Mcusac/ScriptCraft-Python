from pathlib import Path
from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    detect_environment,
    WorkspacePathResolver,
    WorkspaceConfig,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    merge_workspace_config,
    FrameworkConfig,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import Config


def load_legacy_shaped_config(data: Dict[str, Any], path: Path) -> "Config":
    """
    Load YAML without a top-level ``framework`` key (legacy workspace shapes).

    Supports workspace fields at the root or framework-like keys at the root.
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


def load_unified_config(data: Dict[str, Any], path: Path) -> "Config":
    framework = FrameworkConfig(**data.get("framework", {}))

    active = framework.active_workspace
    workspace_data = data.get("workspaces", {}).get(active, {})
    workspace = WorkspaceConfig(**workspace_data)

    env = detect_environment()
    env_data = data.get("environments", {}).get(env, {})

    if env_data:
        workspace = merge_workspace_config(workspace, env_data)

    config = Config(
        framework=framework,
        workspace=workspace,
        tools=data.get("tools", {}),
        pipelines=data.get("pipelines", {}),
        environments=data.get("environments", {}),
        tool_configs=data.get("tool_configs", {}),
    )

    config.workspace_root = path.parent.resolve()
    return config