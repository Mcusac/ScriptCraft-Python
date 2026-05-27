from pathlib import Path
from typing import Any, Dict

from scriptcraft.layers.layer_0_core.level_0 import get_config_value

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.path_resolver import WorkspacePathResolver


def get_tool_config(config: Any, name: str) -> Dict[str, Any]:
    tools = get_config_value(config, "tools", default={})
    if isinstance(tools, dict):
        return dict(tools.get(name, {}))
    tool_section = getattr(config, "tools", None)
    if tool_section is not None and hasattr(tool_section, "get"):
        return dict(tool_section.get(name, {}))
    return {}


def get_pipeline_step(config: Any, name: str) -> Dict[str, Any]:
    pipelines = get_config_value(config, "pipelines", default={})
    if isinstance(pipelines, dict):
        return dict(pipelines.get(name, {}))
    pipeline_section = getattr(config, "pipelines", None)
    if pipeline_section is not None and hasattr(pipeline_section, "get"):
        return dict(pipeline_section.get(name, {}))
    return {}


def get_logging_config(config: Any) -> Any:
    return get_config_value(config, "logging", default=getattr(config, "logging", {}))


def get_project_config(config: Any) -> Dict[str, Any]:
    return {
        "project_name": get_config_value(
            config, "project_name", default=getattr(config, "project_name", "Release Workspace")
        ),
        "version": get_config_value(config, "version", default=getattr(config, "version", "")),
    }


def get_template_config(config: Any) -> Dict[str, Any]:
    template = get_config_value(config, "template", default=getattr(config, "template", {}))
    return template if isinstance(template, dict) else {}


def get_workspace_root(config: Any) -> Path:
    root = get_config_value(config, "workspace_root", default=getattr(config, "workspace_root", None))
    return root if isinstance(root, Path) else Path.cwd()


def get_path_resolver(config: Any):
    resolver = getattr(config, "_path_resolver", None)
    if resolver:
        return resolver

    root = get_workspace_root(config)
    resolver = WorkspacePathResolver(root)
    setattr(config, "_path_resolver", resolver)
    return resolver


def validate_config(config: Any) -> bool:
    workspace = get_config_value(config, "workspace", default=getattr(config, "workspace", None))
    study_name = (
        get_config_value(workspace, "study_name", default=None)
        if workspace is not None
        else None
    )
    if study_name is None and workspace is not None:
        study_name = getattr(workspace, "study_name", None)

    domains = (
        get_config_value(workspace, "domains", default=None)
        if workspace is not None
        else None
    )
    if domains is None and workspace is not None:
        domains = getattr(workspace, "domains", None)

    if not study_name:
        return False

    if domains is not None and isinstance(domains, list) and len(domains) == 0:
        return True

    return True
