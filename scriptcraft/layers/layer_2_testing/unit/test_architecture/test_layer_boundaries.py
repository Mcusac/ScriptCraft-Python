"""Architecture guardrails for layer_1_tools dependency direction."""
import ast
import pytest

from pathlib import Path

_LAYER_1_TOOLS = Path(__file__).resolve().parents[3] / "layer_1_tools"
_INFRA_ROOT = _LAYER_1_TOOLS / "level_0_infra"
_IMPL_ROOT = _LAYER_1_TOOLS / "level_1_impl"
_LEVEL_Z = _IMPL_ROOT / "level_Z"


def _python_files(root: Path) -> list[Path]:
  return [p for p in root.rglob("*.py") if p.is_file()]


def _imports_in_file(path: Path) -> list[str]:
  tree = ast.parse(path.read_text(encoding="utf-8"))
  imports: list[str] = []
  for node in ast.walk(tree):
    if isinstance(node, ast.Import):
      imports.extend(alias.name for alias in node.names)
    elif isinstance(node, ast.ImportFrom) and node.module:
      imports.append(node.module)
  return imports


@pytest.mark.parametrize("path", _python_files(_INFRA_ROOT))
def test_infra_does_not_import_level_1_impl(path: Path) -> None:
  if "level_2_testing" in str(path):
    pytest.skip("test tree")
  for module in _imports_in_file(path):
    assert "level_1_impl" not in module, (
      f"{path.relative_to(_LAYER_1_TOOLS)} imports impl: {module}"
    )


def test_new_infra_modules_exist() -> None:
  expected = [
    _INFRA_ROOT / "level_1" / "tool_run_executor.py",
    _INFRA_ROOT / "level_3" / "comparison_executor.py",
    _INFRA_ROOT / "level_4" / "release_subcommands_cli.py",
  ]
  for path in expected:
    assert path.is_file(), f"Missing canonical module: {path}"


def test_removed_shims_are_gone() -> None:
  removed = [
    _IMPL_ROOT / "level_1" / "release_cli.py",
    _INFRA_ROOT / "level_0" / "mode_runner.py",
    _INFRA_ROOT / "level_1" / "run_context.py",
    _INFRA_ROOT / "level_0" / "tabular_files.py",
    _INFRA_ROOT / "level_0" / "comparison_core.py",
    _INFRA_ROOT / "level_0" / "dataframe_primitives.py",
    _INFRA_ROOT / "level_0" / "schema_contracts.py",
    _INFRA_ROOT / "level_0" / "logging_config_model.py",
    _INFRA_ROOT / "level_0" / "runtime" / "protocols.py",
    _INFRA_ROOT / "level_2" / "value_cleaning.py",
    _INFRA_ROOT / "level_2" / "runtime_loops.py",
    _INFRA_ROOT / "level_1" / "workflow_registry.py",
    _INFRA_ROOT / "level_1" / "mode_runner.py",
    _INFRA_ROOT / "level_1" / "data_loading.py",
    _INFRA_ROOT / "level_1" / "pipeline_execution.py",
    _INFRA_ROOT / "level_1" / "subprocess" / "runner.py",
    _INFRA_ROOT / "level_2" / "mode_runner.py",
    _INFRA_ROOT / "level_2" / "run_context.py",
    _INFRA_ROOT / "level_2" / "comparison_executor.py",
    _INFRA_ROOT / "level_7" / "tool_run_executor.py",
  ]
  for path in removed:
    assert not path.is_file(), f"Shim or stale module still present: {path}"


def test_mode_registry_used_by_comparer_plugins() -> None:
  plugins_path = _IMPL_ROOT / "level_2" / "data_content_comparer" / "plugins.py"
  source = plugins_path.read_text(encoding="utf-8")
  assert "ModeRegistry" in source
  assert "MODE_REGISTRY = ModeRegistry()" in source
  assert "layer_0_core.level_1.runtime.mode_execution" in source


def test_schema_detector_entrypoint_at_level_2() -> None:
  entrypoint = _IMPL_ROOT / "level_2" / "schema_detector" / "entrypoint.py"
  assert entrypoint.is_file(), f"Missing entrypoint: {entrypoint}"
