"""Architecture guardrails for layer_1_tools dependency direction."""
import ast
import pytest

from pathlib import Path

_LAYER_1_TOOLS = Path(__file__).resolve().parents[3] / "layer_1_tools"
_INFRA_ROOT = _LAYER_1_TOOLS / "level_0_infra"
_IMPL_ROOT = _LAYER_1_TOOLS / "level_1_impl"
_LEVEL_Z = _IMPL_ROOT / "level_Z"
_FORBIDDEN_IMPL_PREFIX = "scriptcraft.layers.layer_1_tools.level_1_impl"
_INFRA_PKG_PREFIX = "scriptcraft.layers.layer_1_tools.level_0_infra"
_FORBIDDEN_LEGACY_INFRA_MODULES = (
    f"{_INFRA_PKG_PREFIX}.level_1.config_loader",
    f"{_INFRA_PKG_PREFIX}.level_2.legacy_api",
    f"{_INFRA_PKG_PREFIX}.level_2.comparison",
    f"{_INFRA_PKG_PREFIX}.level_2.pipeline_base",
    f"{_INFRA_PKG_PREFIX}.level_2.dataframe_compare_ops",
    f"{_INFRA_PKG_PREFIX}.level_2.comparison_result",
    f"{_INFRA_PKG_PREFIX}.level_9.tool_dispatch",
    f"{_INFRA_PKG_PREFIX}.level_10.tool_dispatch",
    f"{_INFRA_PKG_PREFIX}.level_0.tool_lookup",
)


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


def _infra_level_from_path(path: Path) -> int | None:
  try:
    first = path.relative_to(_INFRA_ROOT).parts[0]
  except ValueError:
    return None
  if first.startswith("level_") and first[6:].isdigit():
    return int(first[6:])
  return None


def _infra_level_from_module(module: str) -> int | None:
  if not module.startswith(f"{_INFRA_PKG_PREFIX}.level_"):
    return None
  tail = module[len(_INFRA_PKG_PREFIX) + 1 :]
  head = tail.split(".", 1)[0]
  if head.startswith("level_") and head[6:].isdigit():
    return int(head[6:])
  return None


@pytest.mark.parametrize("path", _python_files(_INFRA_ROOT))
def test_infra_does_not_import_level_1_impl(path: Path) -> None:
  if "level_2_testing" in str(path):
    pytest.skip("test tree")
  for module in _imports_in_file(path):
    if not module:
      continue
    if module == _FORBIDDEN_IMPL_PREFIX or module.startswith(
      f"{_FORBIDDEN_IMPL_PREFIX}."
    ):
      pytest.fail(
        f"{path.relative_to(_LAYER_1_TOOLS)} imports impl: {module}"
      )


# Pre-existing upward imports; do not add new entries without a remediation plan.
_KNOWN_INFRA_UPWARD_IMPORTS: set[tuple[str, str]] = {
  (
    "level_0_infra/level_1/discovery_defaults.py",
    "scriptcraft.layers.layer_1_tools.level_0_infra.level_8.registry",
  ),
  (
    "level_0_infra/level_1/io_mixin.py",
    "scriptcraft.layers.layer_1_tools.level_0_infra.level_6",
  ),
  (
    "level_0_infra/level_1/processor.py",
    "scriptcraft.layers.layer_1_tools.level_0_infra.level_6",
  ),
  (
    "level_0_infra/level_2/environment_mixin.py",
    "scriptcraft.layers.layer_1_tools.level_0_infra.level_6",
  ),
  (
    "level_0_infra/level_2/root_schema.py",
    "scriptcraft.layers.layer_1_tools.level_0_infra.level_5.config",
  ),
}


def _collect_infra_upward_imports() -> set[tuple[str, str]]:
  violations: set[tuple[str, str]] = set()
  for path in _python_files(_INFRA_ROOT):
    if "level_2_testing" in str(path):
      continue
    source_level = _infra_level_from_path(path)
    if source_level is None:
      continue
    rel = path.relative_to(_LAYER_1_TOOLS).as_posix()
    for module in _imports_in_file(path):
      imported_level = _infra_level_from_module(module)
      if imported_level is None or imported_level <= source_level:
        continue
      violations.add((rel, module))
  return violations


def test_infra_upward_imports_match_known_allowlist() -> None:
  violations = _collect_infra_upward_imports()
  assert violations == _KNOWN_INFRA_UPWARD_IMPORTS, (
    "Infra upward-import set changed. "
    f"new={violations - _KNOWN_INFRA_UPWARD_IMPORTS} "
    f"removed={_KNOWN_INFRA_UPWARD_IMPORTS - violations}"
  )


@pytest.mark.parametrize("path", _python_files(_INFRA_ROOT))
def test_infra_dispatch_stack_respects_level_ordering(path: Path) -> None:
  """Phase 4/5 dispatch/registry/CLI tiers must not import upward."""
  if "level_2_testing" in str(path):
    pytest.skip("test tree")
  source_level = _infra_level_from_path(path)
  if source_level is None or source_level < 9:
    pytest.skip("dispatch stack levels only")
  for module in _imports_in_file(path):
    imported_level = _infra_level_from_module(module)
    if imported_level is None:
      continue
    if imported_level > source_level:
      pytest.fail(
        f"{path.relative_to(_LAYER_1_TOOLS)} (level_{source_level}) "
        f"imports higher infra level_{imported_level}: {module}"
      )


@pytest.mark.parametrize(
  "path", _python_files(_INFRA_ROOT) + _python_files(_IMPL_ROOT)
)
def test_no_legacy_infra_import_paths(path: Path) -> None:
  if "level_2_testing" in str(path):
    pytest.skip("test tree")
  for module in _imports_in_file(path):
    for forbidden in _FORBIDDEN_LEGACY_INFRA_MODULES:
      if module == forbidden or module.startswith(f"{forbidden}."):
        pytest.fail(
          f"{path.relative_to(_LAYER_1_TOOLS)} uses legacy import: {module}"
        )


def test_phase4_split_facades_removed() -> None:
  """Phase 4 split modules are canonical; re-export shims removed (Phase 6 hygiene)."""
  for name in (
    "comparison.py",
    "pipeline_base.py",
    "dataframe_compare_ops.py",
    "comparison_result.py",
  ):
    assert not (_INFRA_ROOT / "level_2" / name).exists(), (
      f"Remove pointless facade shim: level_2/{name}; import from level_2 barrel or core"
    )


def test_new_infra_modules_exist() -> None:
  expected = [
    _INFRA_ROOT / "level_1" / "tool_run_executor.py",
    _INFRA_ROOT / "level_3" / "dataframe_comparer.py",
    _INFRA_ROOT / "level_4" / "comparison_executor.py",
    _INFRA_ROOT / "level_5" / "release_pipelines" / "release_subcommands_cli.py",
    _INFRA_ROOT / "level_5" / "release_pipelines" / "cli.py",
  ]
  for path in expected:
    assert path.is_file(), f"Missing canonical module: {path}"


def test_tool_lookup_lives_at_level_10_not_level_0() -> None:
  assert not (_INFRA_ROOT / "level_0" / "tool_lookup.py").exists()
  assert not (_INFRA_ROOT / "level_9" / "tool_lookup.py").exists()
  assert (_INFRA_ROOT / "level_10" / "tool_lookup.py").is_file()


def test_infra_root_barrel_has_no_invalid_subpackages() -> None:
  source = (_INFRA_ROOT / "__init__.py").read_text(encoding="utf-8")
  assert "level_1_impl" not in source


def test_cli_lives_at_level_12_not_level_10_or_9() -> None:
  assert not (_INFRA_ROOT / "level_9" / "cli.py").exists()
  assert not (_INFRA_ROOT / "level_10" / "cli.py").exists()
  assert (_INFRA_ROOT / "level_12" / "cli.py").is_file()
  assert (_INFRA_ROOT / "level_11" / "tool_dispatch.py").is_file()


def test_discovery_engine_has_no_hardcoded_impl_prefix() -> None:
  source = (_INFRA_ROOT / "level_7" / "discovery.py").read_text(encoding="utf-8")
  assert "level_1_impl" not in source


def test_removed_shims_are_gone() -> None:
  removed = [
    _INFRA_ROOT / "level_0" / "tool_lookup.py",
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
    _INFRA_ROOT / "level_2" / "comparison.py",
    _INFRA_ROOT / "level_2" / "pipeline_base.py",
    _INFRA_ROOT / "level_2" / "dataframe_compare_ops.py",
    _INFRA_ROOT / "level_2" / "comparison_result.py",
    _INFRA_ROOT / "level_7" / "tool_run_executor.py",
    _IMPL_ROOT / "level_0" / "release_manager_plugins",
    _IMPL_ROOT / "level_1" / "release_manager_plugins",
    _IMPL_ROOT / "level_0" / "release_manager_plugins" / "workspace_release_mode.py",
    _IMPL_ROOT / "level_1" / "release_manager_plugins" / "workspace_plugin.py",
  ]
  for path in removed:
    assert not path.exists(), f"Shim or stale module still present: {path}"


def test_mode_registry_used_by_comparer_plugins() -> None:
  plugins_path = _IMPL_ROOT / "level_2" / "data_content_comparer" / "plugins.py"
  source = plugins_path.read_text(encoding="utf-8")
  assert "ModeRegistry" in source
  assert "MODE_REGISTRY = ModeRegistry()" in source
  assert "layer_0_core.level_1.runtime.mode_execution" in source


def test_phase1_tool_entrypoints_exist() -> None:
  comparer_entry = _IMPL_ROOT / "level_4" / "data_content_comparer" / "entrypoint.py"
  release_cli = _IMPL_ROOT / "level_6" / "release_manager" / "cli.py"
  assert comparer_entry.is_file(), f"Missing entrypoint: {comparer_entry}"
  assert release_cli.is_file(), f"Missing CLI: {release_cli}"


def test_phase2_normalized_tool_entrypoints_exist() -> None:
  expected = [
    _IMPL_ROOT / "level_1" / "asset_updater" / "entrypoint.py",
    _IMPL_ROOT / "level_1" / "asset_reconciliation" / "entrypoint.py",
    _IMPL_ROOT / "level_2" / "medvisit_integrity_validator" / "entrypoint.py",
    _IMPL_ROOT / "level_2" / "dictionary_validator" / "entrypoint.py",
    _IMPL_ROOT / "level_1" / "git_workspace_tool" / "entrypoint.py",
  ]
  for entry in expected:
    assert entry.is_file(), f"Missing normalized entrypoint: {entry}"

  removed_shims = [
    _IMPL_ROOT / "level_4" / "asset_updater" / "entrypoint.py",
    _IMPL_ROOT / "level_1" / "rhq_form_autofiller" / "cli.py",
    _IMPL_ROOT / "level_0" / "dictionary_validator_main.py",
    _IMPL_ROOT / "level_0" / "feature_change_checker_main.py",
  ]
  for path in removed_shims:
    assert not path.exists(), f"Shim should be removed: {path}"


def test_phase8_legacy_loader_module_removed() -> None:
  legacy = _INFRA_ROOT / "level_3" / "legacy_loader.py"
  assert not legacy.exists(), f"legacy_loader.py must be removed: {legacy}"


def test_phase5_legacy_config_modules_removed() -> None:
  removed = [
    _INFRA_ROOT / "level_1" / "config_loader.py",
    _INFRA_ROOT / "level_2" / "legacy_api.py",
  ]
  for path in removed:
    assert not path.exists(), f"Legacy config module still present: {path}"


def test_phase5_cli_uses_canonical_dispatch() -> None:
  source = (_INFRA_ROOT / "level_12" / "cli.py").read_text(encoding="utf-8")
  assert "dispatch_tool_by_name" in source
  assert "tool_instance.run()" not in source


def test_phase5_level11_exports_dispatch_tool_by_name() -> None:
  source = (_INFRA_ROOT / "level_11" / "__init__.py").read_text(encoding="utf-8")
  assert "dispatch_tool_by_name" in source


def test_phase5_level10_does_not_export_dispatch_tool_by_name() -> None:
  source = (_INFRA_ROOT / "level_10" / "__init__.py").read_text(encoding="utf-8")
  assert "dispatch_tool_by_name" not in source
  assert '"dispatch_tool"' not in source


def test_phase5_tool_metadata_uses_shared_impl_roots() -> None:
  source = (_INFRA_ROOT / "level_2" / "tool_metadata.py").read_text(encoding="utf-8")
  assert "DEFAULT_TOOL_MODULE_PREFIX" in source
  assert "level_1_impl" not in source


def test_phase5_scriptcraft_console_entrypoint() -> None:
  pyproject = _LAYER_1_TOOLS.parents[2] / "pyproject.toml"
  content = pyproject.read_text(encoding="utf-8")
  assert (
    'scriptcraft = "scriptcraft.layers.layer_1_tools.level_0_infra.level_12.cli:main"'
    in content
  )


def test_phase5_level11_dispatch_and_level0_impl_roots_exist() -> None:
  assert (_INFRA_ROOT / "level_11" / "tool_dispatch.py").is_file()
  assert (_INFRA_ROOT / "level_10" / "tool_lookup.py").is_file()
  assert (_INFRA_ROOT / "level_0" / "impl_tool_roots.py").is_file()
  assert (_INFRA_ROOT / "level_1" / "discovery_defaults.py").is_file()
  assert not (_INFRA_ROOT / "level_10" / "tool_dispatch.py").exists()
  assert not (_INFRA_ROOT / "level_9" / "tool_dispatch.py").exists()
  assert not (_INFRA_ROOT / "level_1" / "impl_tool_roots.py").exists()


def test_phase5_runner_lives_at_level_6() -> None:
  assert (_INFRA_ROOT / "level_6" / "runner.py").is_file()
  assert not (_INFRA_ROOT / "level_4" / "runner.py").exists()


def test_phase5_cli_uses_canonical_discovery_bootstrap() -> None:
  source = (_INFRA_ROOT / "level_12" / "cli.py").read_text(encoding="utf-8")
  assert "ensure_tools_discovered" in source
  assert "unified_registry.discover_tools(" not in source


def test_phase5_deprecated_aliases_not_exported_from_level_2() -> None:
  source = (_INFRA_ROOT / "level_2" / "__init__.py").read_text(encoding="utf-8")
  for symbol in (
    "BasePipeline",
    "QCPipelineEngine",
    "standardize_tool_execution",
  ):
    assert f'"{symbol}"' not in source


def test_phase5_root_barrel_does_not_star_export_dispatch_levels() -> None:
  source = (_INFRA_ROOT / "__init__.py").read_text(encoding="utf-8")
  assert "from .level_10 import *" not in source
  assert "from .level_11 import *" not in source
  assert "from .level_12 import *" not in source
  assert "dispatch_tool_by_name" not in source


def _relative_imports_in_logic_files(root: Path) -> list[tuple[str, int]]:
  violations: list[tuple[str, int]] = []
  for path in _python_files(root):
    if "level_2_testing" in str(path):
      continue
    if path.name == "__init__.py":
      continue
    tree = ast.parse(path.read_text(encoding="utf-8"))
    rel = path.relative_to(_LAYER_1_TOOLS).as_posix()
    for node in ast.walk(tree):
      if isinstance(node, ast.ImportFrom) and node.level and node.level > 0:
        violations.append((rel, node.lineno or 0))
  return violations


def test_logic_files_do_not_use_relative_imports_in_infra_or_impl() -> None:
  violations = _relative_imports_in_logic_files(_INFRA_ROOT)
  violations.extend(_relative_imports_in_logic_files(_IMPL_ROOT))
  assert violations == [], (
    "Relative imports are allowed only in __init__.py. Violations: "
    + ", ".join(f"{path}:{line}" for path, line in violations)
  )


def _owner_impl_level(path: Path) -> int | None:
  try:
    rel = path.relative_to(_IMPL_ROOT)
  except ValueError:
    return None
  head = rel.parts[0]
  if head.startswith("level_") and head[6:].isdigit():
    return int(head[6:])
  return None


def _imported_impl_level(module: str) -> int | None:
  prefix = f"{_FORBIDDEN_IMPL_PREFIX}.level_"
  if not module.startswith(prefix):
    return None
  level_segment = module[len(prefix) :].split(".", 1)[0]
  if level_segment.startswith("level_") and level_segment[6:].isdigit():
    return int(level_segment[6:])
  return None


def test_impl_same_tree_imports_do_not_point_upward() -> None:
  violations: list[str] = []
  for path in _python_files(_IMPL_ROOT):
    if "level_2_testing" in str(path):
      continue
    owner_level = _owner_impl_level(path)
    if owner_level is None:
      continue
    rel = path.relative_to(_LAYER_1_TOOLS).as_posix()
    for module in _imports_in_file(path):
      imported_level = _imported_impl_level(module)
      if imported_level is not None and imported_level >= owner_level:
        violations.append(f"{rel} imports {module}")
  assert violations == [], (
    "Impl modules must not import same-tree levels at or above their tier: "
    + "; ".join(violations)
  )
