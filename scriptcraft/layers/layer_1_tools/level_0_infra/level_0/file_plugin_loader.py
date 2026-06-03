"""Generic file-based workflow plugin loading (registry-protocol based)."""

import importlib.util

from pathlib import Path
from typing import Any, Callable, Protocol


class PluginWorkflowRegistryProtocol(Protocol):
    def has_workflow(self, name: str) -> bool: ...

    def register_workflow(
        self,
        name: str,
        workflow: Callable[..., Any],
        info: dict[str, Any],
    ) -> None: ...


def load_module_from_path(path: Path, *, module_prefix: str = "file_plugin") -> Any:
    module_name = f"{module_prefix}_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load plugin module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_plugin_contract(
    module: Any,
    *,
    mode_attr: str,
    workflow_attr: str,
    info_attr: str,
) -> tuple[str, Callable[..., Any], dict[str, Any]]:
    if not hasattr(module, mode_attr):
        raise ValueError(f"Plugin module missing required attribute: {mode_attr}")
    if not hasattr(module, workflow_attr):
        raise ValueError(f"Plugin module missing required attribute: {workflow_attr}")

    mode = getattr(module, mode_attr)
    workflow = getattr(module, workflow_attr)
    info = getattr(module, info_attr, {}) or {}

    if not isinstance(mode, str) or not mode.strip():
        raise ValueError(f"{mode_attr} must be a non-empty string")
    if not callable(workflow):
        raise ValueError(f"{workflow_attr} must be callable")
    if not isinstance(info, dict):
        raise ValueError(f"{info_attr} must be a dict when provided")

    return mode.strip(), workflow, info


def load_plugins(
    registry: PluginWorkflowRegistryProtocol,
    plugins_dir: Path,
    *,
    pattern: str = "*.py",
    mode_attr: str = "MODE",
    workflow_attr: str = "WORKFLOW",
    info_attr: str = "INFO",
    on_message: Callable[[str], None] | None = None,
) -> int:
    """
    Load workflow plugins from ``plugins_dir`` and register them on ``registry``.

    Per-file failures invoke ``on_message`` when provided and are skipped.
    Returns count of successfully loaded plugins.
    """
    emit = on_message or (lambda _msg: None)

    if not plugins_dir.is_dir():
        emit(f"Plugin directory not found: {plugins_dir}")
        return 0

    loaded = 0
    for path in sorted(plugins_dir.glob(pattern)):
        if not path.is_file():
            continue
        try:
            module = load_module_from_path(path)
            mode, workflow, info = extract_plugin_contract(
                module,
                mode_attr=mode_attr,
                workflow_attr=workflow_attr,
                info_attr=info_attr,
            )
            if registry.has_workflow(mode):
                emit(f"Skipping duplicate workflow mode: {mode} ({path.name})")
                continue
            registry.register_workflow(mode, workflow, info)
            loaded += 1
            emit(f"Loaded plugin: {mode} ({path.name})")
        except Exception as exc:
            emit(
                f"Failed to load plugin {path.name}: "
                f"{type(exc).__name__}: {exc}"
            )
    return loaded
