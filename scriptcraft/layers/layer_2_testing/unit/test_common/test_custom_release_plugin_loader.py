"""Tests for custom release plugin loader contract."""

import importlib.util
import sys
from pathlib import Path

import pytest

_PKG_ROOT = Path(__file__).resolve().parents[3]
_LOADER_PATH = _PKG_ROOT / "level_1_impl" / "level_0" / "release_manager" / "custom_plugin_loader.py"
_REGISTRY_PATH = _PKG_ROOT / "level_1_impl" / "level_0" / "release_manager_plugins" / "registry.py"


def _load_loader():
  import types

  log_stub = types.ModuleType("scriptcraft.layers.layer_1_tools.level_0_infra.level_0")
  log_stub.log_and_print = lambda msg, level="info": None
  sys.modules[log_stub.__name__] = log_stub

  spec = importlib.util.spec_from_file_location(
    "release_manager_custom_plugin_loader",
    _LOADER_PATH,
  )
  module = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(module)
  return module


def test_extract_plugin_contract_requires_mode_and_workflow(tmp_path: Path) -> None:
  loader = _load_loader()
  bad = tmp_path / "custom_bad.py"
  bad.write_text("RELEASE_MODE = ''\n", encoding="utf-8")
  spec = importlib.util.spec_from_file_location("custom_bad", bad)
  mod = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(mod)

  with pytest.raises(ValueError):
    loader._extract_plugin_contract(mod, bad)


def test_load_custom_plugins_registers_valid_plugin(tmp_path: Path) -> None:
  loader = _load_loader()
  plugins_dir = tmp_path / "plugins"
  plugins_dir.mkdir()
  plugin_file = plugins_dir / "custom_demo.py"
  plugin_file.write_text(
    """
RELEASE_MODE = "demo_custom"
def RELEASE_WORKFLOW(**kwargs):
    return None
RELEASE_INFO = {"description": "demo"}
""",
    encoding="utf-8",
  )

  registry_mod = importlib.util.spec_from_file_location("registry", _REGISTRY_PATH)
  registry_module = importlib.util.module_from_spec(registry_mod)
  assert registry_mod.loader is not None
  registry_mod.loader.exec_module(registry_module)
  registry = registry_module.ReleaseWorkflowRegistry()

  count = loader.load_custom_plugins(registry, plugins_dir)
  assert count == 1
  assert registry.has_workflow("demo_custom")
  assert registry.get_workflow("demo_custom") is not None
