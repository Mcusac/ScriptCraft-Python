"""Discover and register custom release workflow plugins from a local plugins directory."""

import importlib.util

from pathlib import Path
from typing import Any, Callable, Dict, Tuple

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print


# Contract: each custom_*.py module must define these attributes.
MODE_ATTR = "RELEASE_MODE"
WORKFLOW_ATTR = "RELEASE_WORKFLOW"
INFO_ATTR = "RELEASE_INFO"


def _load_module_from_path(plugin_file: Path, module_name: str):
  spec = importlib.util.spec_from_file_location(module_name, plugin_file)
  if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load plugin module: {plugin_file}")
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


def _extract_plugin_contract(module: Any, plugin_file: Path) -> Tuple[str, Callable, Dict[str, Any]]:
  mode = getattr(module, MODE_ATTR, None)
  workflow = getattr(module, WORKFLOW_ATTR, None)

  if not isinstance(mode, str) or not mode.strip():
    raise ValueError(f"{plugin_file.name}: {MODE_ATTR} must be a non-empty string")
  if not callable(workflow):
    raise ValueError(f"{plugin_file.name}: {WORKFLOW_ATTR} must be callable")

  info = getattr(module, INFO_ATTR, None)
  if info is None:
    info = {}
  if not isinstance(info, dict):
    raise ValueError(f"{plugin_file.name}: {INFO_ATTR} must be a dict when provided")

  return mode.strip(), workflow, info


def load_custom_plugins(registry: Any, plugins_dir: Path) -> int:
  """
  Load custom_*.py plugins from plugins_dir into registry.

  Returns count of successfully registered plugins. Per-file failures log warnings only.
  """
  if not plugins_dir.is_dir():
    return 0

  registered = 0
  for plugin_file in sorted(plugins_dir.glob("custom_*.py")):
    if plugin_file.name == "__init__.py":
      continue

    module_name = f"release_manager_custom_{plugin_file.stem}"
    try:
      module = _load_module_from_path(plugin_file, module_name)
      mode, workflow, info = _extract_plugin_contract(module, plugin_file)

      if registry.has_workflow(mode):
        log_and_print(
          f"⚠️ Custom plugin {plugin_file.name}: mode '{mode}' already registered; skipping",
          level="warning",
        )
        continue

      registry.register_workflow(mode, workflow, info)
      log_and_print(f"🔌 Registered custom release workflow: {mode} ({plugin_file.name})")
      registered += 1
    except Exception as e:
      log_and_print(
        f"⚠️ Failed to load custom plugin {plugin_file.name}: {e}",
        level="warning",
      )

  return registered
