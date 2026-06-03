"""Guardrails for infra-to-core drain canonical ownership."""

import ast
import pytest

from pathlib import Path

_LAYER_0_CORE = Path(__file__).resolve().parents[3] / "layer_0_core"
_INFRA_ROOT = Path(__file__).resolve().parents[3] / "layer_1_tools" / "level_0_infra"

_CANONICAL_CORE_MODULES = [
    _LAYER_0_CORE / "level_1" / "runtime" / "mode_execution.py",
    _LAYER_0_CORE / "level_1" / "runtime" / "run_context.py",
    _LAYER_0_CORE / "level_0" / "runtime" / "tool_protocols.py",
    _LAYER_0_CORE / "level_5" / "file_io" / "tabular.py",
    _LAYER_0_CORE / "level_0" / "dataframe_diff.py",
    _LAYER_0_CORE / "level_0" / "dataframe_primitives.py",
    _LAYER_0_CORE / "level_0" / "processing" / "range_membership.py",
    _LAYER_0_CORE / "level_1" / "processing" / "missing_detection.py",
    _LAYER_0_CORE / "level_2" / "processing" / "numeric_validation.py",
    _LAYER_0_CORE / "level_0" / "schema_contracts.py",
    _LAYER_0_CORE / "level_1" / "runtime" / "domain_loops.py",
    _LAYER_0_CORE / "level_1" / "runtime" / "tool_lifecycle.py",
    _LAYER_0_CORE / "level_1" / "runtime" / "retry.py",
]

_REMOVED_INFRA_SHIMS = [
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
]

_INFRA_BARREL_INITS = [
    _INFRA_ROOT / "level_0" / "__init__.py",
    _INFRA_ROOT / "level_1" / "__init__.py",
    _INFRA_ROOT / "level_2" / "__init__.py",
]


def _imports_in_file(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


@pytest.mark.parametrize("path", _CANONICAL_CORE_MODULES)
def test_canonical_core_modules_exist(path: Path) -> None:
    assert path.is_file(), f"Missing canonical core module: {path}"


@pytest.mark.parametrize("path", _REMOVED_INFRA_SHIMS)
def test_infra_shims_are_gone(path: Path) -> None:
    assert not path.is_file(), f"Infra re-export shim still present: {path}"


def test_core_does_not_import_layer_1_tools() -> None:
    for path in _LAYER_0_CORE.rglob("*.py"):
        if not path.is_file():
            continue
        for module in _imports_in_file(path):
            assert "layer_1_tools" not in module, (
                f"{path.relative_to(_LAYER_0_CORE)} imports tools layer: {module}"
            )


@pytest.mark.parametrize("path", _INFRA_BARREL_INITS)
def test_infra_barrels_do_not_reexport_from_core(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    assert "layer_0_core" not in source, (
        f"{path.relative_to(_INFRA_ROOT)} should not re-export from layer_0_core"
    )
