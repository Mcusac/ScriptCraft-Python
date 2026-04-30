from pathlib import Path
from typing import Any, Dict

from layers.layer_1_tools.level_0_infra.level_0.environment import detect_environment
from layers.layer_1_tools.level_0_infra.level_0.workspace_schema import WorkspaceConfig
from layers.layer_1_tools.level_0_infra.level_1.merger import merge_workspace_config
from layers.layer_1_tools.level_0_infra.level_1.framework_schema import FrameworkConfig
from layers.layer_1_tools.level_0_infra.level_2.root_schema import Config


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