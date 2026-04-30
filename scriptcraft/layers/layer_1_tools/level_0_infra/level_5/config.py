"""
Configuration orchestrator.

Focused responsibilities:
- Delegate IO to loaders
- Delegate transforms to services
- Finalize runtime-only fields (workspace_root, path resolver)
"""

from pathlib import Path
from typing import Union

from layers.layer_1_tools.level_0_infra.level_0.path_resolver import WorkspacePathResolver
from layers.layer_1_tools.level_0_infra.level_1.tool_discovery import discover_and_merge_tools
from layers.layer_1_tools.level_0_infra.level_2.root_schema import Config
from layers.layer_1_tools.level_0_infra.level_4.yaml_loader import load_config_from_yaml

# ===== CONVENIENCE FUNCTIONS =====

def load_config(path: Union[str, Path] = "config.yaml") -> Config:
    """Load configuration from YAML file with env fallback."""
    config = load_config_from_yaml(path)
    return finalize_config(config, Path(path))

def get_config() -> Config:
    """Get configuration with default path."""
    return load_config()


def finalize_config(config: Config, config_path: Path) -> Config:
    """
    Populate runtime-only fields that are not part of serialized config data.
    """
    if config.workspace_root is None:
        config.workspace_root = config_path.parent.resolve()

    if config._path_resolver is None and config.workspace_root is not None:
        config._path_resolver = WorkspacePathResolver(config.workspace_root)

    return config


def merge_discovered_tools(
    config: Config,
    discovered_tool_names: list[str],
    *,
    describe_tool=None,
) -> None:
    """
    Merge discovered tool names into the config.

    Discovery itself is orchestration outside this package to avoid circular
    imports and to keep this module import-safe.
    """
    discover_and_merge_tools(
        config,
        discovered_tool_names,
        describe_tool=describe_tool,
    )


 