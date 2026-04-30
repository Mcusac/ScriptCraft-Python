from typing import Dict, Any

from layers.layer_1_tools.level_0_infra.level_0.workspace_schema import WorkspaceConfig


def merge_workspace_config(
    base: WorkspaceConfig,
    override: Dict[str, Any]
) -> WorkspaceConfig:
    data = base.__dict__.copy()

    for k, v in override.items():
        if k in data:
            data[k] = v

    return WorkspaceConfig(**data)