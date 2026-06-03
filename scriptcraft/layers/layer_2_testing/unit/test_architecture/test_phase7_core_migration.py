"""Phase 7 architecture gates for C6-01/C6-02 core promotion."""

from __future__ import annotations

import ast
from pathlib import Path

import pandas as pd
import pytest

_LAYERS = Path(__file__).resolve().parents[3]
_LAYER_0_CORE = _LAYERS / "layer_0_core"
_TOOLS_INFRA = _LAYERS / "layer_1_tools" / "level_0_infra"

_CANONICAL_C6_01 = (
    _LAYER_0_CORE / "level_0" / "validation" / "dataframe_compare_ops.py"
)
_CANONICAL_C6_02 = (
    _LAYER_0_CORE / "level_0" / "validation" / "comparison_result.py"
)

_REMOVED_TOOLS_SHIM_MODULES = (
    "dataframe_compare_ops.py",
    "comparison_result.py",
)

_DATAFRAME_COMPARER = _TOOLS_INFRA / "level_3" / "dataframe_comparer.py"


def _imports_in_file(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def test_phase7_canonical_core_modules_exist() -> None:
    assert _CANONICAL_C6_01.is_file()
    assert _CANONICAL_C6_02.is_file()


def test_phase7_tools_shim_modules_removed() -> None:
    for name in _REMOVED_TOOLS_SHIM_MODULES:
        path = _TOOLS_INFRA / "level_2" / name
        assert not path.exists(), (
            f"{name} must not exist; import from layer_0_core.level_0.validation"
        )


def test_phase7_dataframe_comparer_imports_core_kernels() -> None:
    imports = _imports_in_file(_DATAFRAME_COMPARER)
    assert any(
        m == "scriptcraft.layers.layer_0_core.level_0"
        or m.startswith("scriptcraft.layers.layer_0_core.level_0.")
        for m in imports
    ), "dataframe_comparer must import canonical core validation via level_0 barrel"
    assert not any(
        m.endswith(".level_2.comparison_result")
        or m.endswith(".level_2.dataframe_compare_ops")
        for m in imports
        if m.startswith("scriptcraft.layers.layer_1_tools")
    ), "dataframe_comparer must not import removed tools shim modules"


_COMPARE_SYMBOLS = (
    "column_sets",
    "content_differences",
    "dtype_mismatches",
    "index_sets",
    "shape_mismatch",
    "ComparisonResult",
)


def test_phase8_tools_barrel_does_not_reexport_core_validation() -> None:
    """Phase 8: core kernels import from layer_0_core directly, not level_2 barrel."""
    init_path = _TOOLS_INFRA / "level_2" / "__init__.py"
    text = init_path.read_text(encoding="utf-8")
    assert "layer_0_core.level_0.validation" not in text
    all_section = text.split("__all__", 1)[-1]
    for name in _COMPARE_SYMBOLS:
        assert f'"{name}"' not in all_section, (
            f"{name} must not be re-exported from level_2 barrel"
        )


def test_phase7_validation_barrel_exports_compare_symbols() -> None:
    from scriptcraft.layers.layer_0_core.level_0 import validation

    for name in (
        "column_sets",
        "content_differences",
        "dtype_mismatches",
        "index_sets",
        "shape_mismatch",
        "ComparisonResult",
    ):
        assert name in validation.__all__


def test_phase7_index_sets_partition() -> None:
    from scriptcraft.layers.layer_0_core.level_0.validation import index_sets

    df1 = pd.DataFrame({"a": [1, 2]}, index=[0, 1])
    df2 = pd.DataFrame({"a": [1]}, index=[0])
    common, only_1, only_2 = index_sets(df1, df2)
    assert common == {0}
    assert only_1 == {1}
    assert only_2 == set()


def test_phase7_shape_mismatch_detects_difference() -> None:
    from scriptcraft.layers.layer_0_core.level_0.validation import shape_mismatch

    df1 = pd.DataFrame({"a": [1, 2]})
    df2 = pd.DataFrame({"a": [1]})
    result = shape_mismatch(df1, df2)
    assert result == ((2, 1), (1, 1))


def test_phase7_comparison_result_normalizes_dtype_mismatches() -> None:
    from scriptcraft.layers.layer_0_core.level_0.validation import ComparisonResult

    result = ComparisonResult(
        common=set(),
        only_in_first=set(),
        only_in_second=set(),
        dtype_mismatches=None,
    )
    assert result.dtype_mismatches == {}


def test_phase7_content_differences_when_values_differ() -> None:
    from scriptcraft.layers.layer_0_core.level_0.validation import content_differences

    df1 = pd.DataFrame({"a": [1]})
    df2 = pd.DataFrame({"a": [2]})
    diff = content_differences(df1, df2)
    assert diff is not None
    assert not diff.empty
