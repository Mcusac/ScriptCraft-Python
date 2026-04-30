from pathlib import Path
from typing import Any, Dict

from layers.layer_1_tools.level_0_infra.level_0.path_resolver import create_path_resolver


def get_tool_config(config: Any, name: str) -> Dict[str, Any]:
    return config.tools.get(name, {})


def get_pipeline_step(config: Any, name: str) -> Dict[str, Any]:
    return config.pipelines.get(name, {})


def get_logging_config(config: Any) -> Any:
    return getattr(config, "logging", {})


def get_project_config(config: Any) -> Dict[str, Any]:
    return {
        "project_name": getattr(config, "project_name", "Release Workspace"),
        "version": getattr(config, "version", ""),
    }


def get_template_config(config: Any) -> Dict[str, Any]:
    template = getattr(config, "template", {})
    return template if isinstance(template, dict) else {}


def get_workspace_root(config: Any) -> Path:
    root = getattr(config, "workspace_root", None)
    return root if isinstance(root, Path) else Path.cwd()


def get_path_resolver(config: Any):
    resolver = getattr(config, "_path_resolver", None)
    if resolver:
        return resolver

    root = get_workspace_root(config)
    resolver = create_path_resolver(root)
    setattr(config, "_path_resolver", resolver)
    return resolver


def validate_config(config: Any) -> bool:
    workspace = getattr(config, "workspace", None)
    study_name = getattr(workspace, "study_name", None) if workspace else None
    domains = getattr(workspace, "domains", None) if workspace else None

    if not study_name:
        return False

    if domains is not None and isinstance(domains, list) and len(domains) == 0:
        return True

    return True