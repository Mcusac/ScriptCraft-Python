"""Phase 6 architecture gates for core migration preparation."""

from __future__ import annotations

import ast
import re

from pathlib import Path

import pytest

_LAYERS = Path(__file__).resolve().parents[3]
_LAYER_0_CORE = _LAYERS / "layer_0_core"
_LAYER_1_TOOLS = _LAYERS / "layer_1_tools"
_TOOLS_INFRA = _LAYER_1_TOOLS / "level_0_infra"
_DOCS = _LAYER_1_TOOLS / "docs"

_PHASE8_DOC = _DOCS / "ARCHITECTURE_phase8.md"

_FORBIDDEN_UPPER_IMPORTS = (
    "scriptcraft.layers.layer_1_tools",
    "scriptcraft.layers.layer_1_competition",
    "scriptcraft.layers.layer_2_devtools",
)

_TOOL_DOMAIN_TERMS = (
    "workspace",
    "release",
    "rhq",
    "dictionary",
    "med_id",
    "visit_id",
    "tool_name",
)

# Phase 7 canonical kernel modules (core paths).
_P0_KERNEL_MODULES = (
    _LAYER_0_CORE / "level_0" / "validation" / "dataframe_compare_ops.py",
    _LAYER_0_CORE / "level_0" / "validation" / "comparison_result.py",
)

# Phase 4/7 re-export shim modules removed; consumers use level_2 barrel or core paths.
_REMOVED_LEVEL_2_SHIMS = (
    "comparison.py",
    "pipeline_base.py",
    "dataframe_compare_ops.py",
    "comparison_result.py",
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


def _public_definitions(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(node.name)
    return names


@pytest.mark.parametrize("path", _python_files(_LAYER_0_CORE))
def test_core_does_not_import_tools_layers(path: Path) -> None:
    if "layer_2_testing" in str(path):
        pytest.skip("test tree")
    for module in _imports_in_file(path):
        if not module:
            continue
        for forbidden in _FORBIDDEN_UPPER_IMPORTS:
            if module == forbidden or module.startswith(f"{forbidden}."):
                pytest.fail(
                    f"{path.relative_to(_LAYERS)} imports upper layer: {module}"
                )


def test_phase6_inventory_doc_exists() -> None:
    assert _PHASE8_DOC.is_file(), f"Missing Phase 8 architecture doc: {_PHASE8_DOC}"


def test_phase6_preflight_closeout_doc_exists() -> None:
    assert _PHASE8_DOC.is_file(), f"Missing Phase 8 architecture doc: {_PHASE8_DOC}"


def test_phase6_p0_kernel_modules_exist() -> None:
    for path in _P0_KERNEL_MODULES:
        assert path.is_file(), f"Missing P0 kernel module: {path}"


@pytest.mark.parametrize("path", _P0_KERNEL_MODULES)
def test_phase6_p0_kernels_have_no_tools_imports(path: Path) -> None:
    for module in _imports_in_file(path):
        if module.startswith("scriptcraft.layers.layer_1_tools"):
            pytest.fail(f"{path.name} must not import layer_1_tools: {module}")


@pytest.mark.parametrize("path", _P0_KERNEL_MODULES)
def test_phase6_p0_public_api_avoids_tool_domain_terms(path: Path) -> None:
    for name in _public_definitions(path):
        lowered = name.lower()
        for term in _TOOL_DOMAIN_TERMS:
            assert term not in lowered, (
                f"{path.name} public symbol {name!r} contains tool-domain term {term!r}"
            )


def test_phase6_level2_reexport_shims_removed() -> None:
    for name in _REMOVED_LEVEL_2_SHIMS:
        path = _TOOLS_INFRA / "level_2" / name
        assert not path.exists(), (
            f"{name} must not exist; import from level_2 barrel or canonical submodule"
        )


def test_phase6_doc_documents_naming_collisions() -> None:
    text = _PHASE8_DOC.read_text(encoding="utf-8")
    for symbol in ("BasePipeline", "PathConfig", "Config"):
        assert symbol in text, f"Phase 6 doc must document naming collision for {symbol}"


def test_phase6_doc_lists_phase7_ready_candidates() -> None:
    text = _PHASE8_DOC.read_text(encoding="utf-8")
    assert "C6-01" in text
    assert "C6-02" in text
    assert "Phase 7-ready" in text


def test_phase6_doc_defines_regression_bundle() -> None:
    text = _PHASE8_DOC.read_text(encoding="utf-8")
    assert "test_phase6_core_candidates.py" in text
    assert "test_phase7_core_migration.py" in text


def test_phase6_naming_matrix_forbids_ambiguous_basepipeline_guidance() -> None:
    text = _PHASE8_DOC.read_text(encoding="utf-8")
    assert "LifecyclePipelineBase" in text
    assert "StepPipelineEngine" in text
    assert re.search(r"Never merge", text, re.IGNORECASE)
