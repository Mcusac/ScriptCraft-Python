"""Phase 3 architecture gates for infra candidate modules."""

from __future__ import annotations

import ast

from pathlib import Path


_LAYER_1_TOOLS = Path(__file__).resolve().parents[3] / "layer_1_tools"
_IMPL_ROOT = _LAYER_1_TOOLS / "level_1_impl"
_INFRA_ROOT = _LAYER_1_TOOLS / "level_0_infra"
_FORBIDDEN_IMPL_PREFIX = "scriptcraft.layers.layer_1_tools.level_1_impl"

_CANDIDATE_REGISTRY = (
    _IMPL_ROOT / "level_0" / "release_manager" / "registry.py"
)
_CANDIDATE_CUSTOM_LOADER = (
    _IMPL_ROOT / "level_0" / "release_manager" / "custom_plugin_loader.py"
)
_CANDIDATE_DICTIONARY_RUNNER = (
    _IMPL_ROOT / "level_1" / "dictionary_driven_checker" / "runner.py"
)


def _imports_in_file(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def _has_top_level_call(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Expr):
            value = node.value
            if isinstance(value, ast.Call):
                return True
    return False


def _owner_impl_level(path: Path) -> int:
    for part in path.parts:
        if part.startswith("level_") and part[6:].isdigit():
            return int(part[6:])
    raise ValueError(f"Could not determine impl level from path: {path}")


def _imported_impl_level(module: str) -> int | None:
    prefix = f"{_FORBIDDEN_IMPL_PREFIX}.level_"
    if not module.startswith(prefix):
        return None
    level_segment = module[len(prefix) :].split(".", 1)[0]
    if level_segment.startswith("level_") and level_segment[6:].isdigit():
        return int(level_segment[6:])
    return None


def test_phase3_candidate_modules_exist() -> None:
    for path in (
        _CANDIDATE_REGISTRY,
        _CANDIDATE_CUSTOM_LOADER,
        _CANDIDATE_DICTIONARY_RUNNER,
    ):
        assert path.is_file(), f"Missing Phase 3 candidate module: {path}"


def test_phase3_candidates_do_not_import_upper_impl_layers() -> None:
    for path in (
        _CANDIDATE_REGISTRY,
        _CANDIDATE_CUSTOM_LOADER,
        _CANDIDATE_DICTIONARY_RUNNER,
    ):
        owner_level = _owner_impl_level(path)
        for module in _imports_in_file(path):
            if module == _FORBIDDEN_IMPL_PREFIX:
                raise AssertionError(
                    f"{path.relative_to(_LAYER_1_TOOLS)} imports impl root: {module}"
                )
            imported_level = _imported_impl_level(module)
            if imported_level is not None and imported_level >= owner_level:
                raise AssertionError(
                    f"{path.relative_to(_LAYER_1_TOOLS)} imports impl module: {module}"
                )


def test_custom_plugin_loader_has_no_import_time_side_effect_calls() -> None:
    assert not _has_top_level_call(_CANDIDATE_CUSTOM_LOADER), (
        "custom_plugin_loader.py must remain side-effect free at import time"
    )


def test_custom_plugin_loader_is_registry_interface_based() -> None:
    source = _CANDIDATE_CUSTOM_LOADER.read_text(encoding="utf-8")
    assert "ReleaseWorkflowRegistry" not in source


def test_file_plugin_loader_extracted_to_infra() -> None:
    infra_loader = _INFRA_ROOT / "level_0" / "file_plugin_loader.py"
    assert infra_loader.is_file()
    source = _CANDIDATE_CUSTOM_LOADER.read_text(encoding="utf-8")
    assert "load_plugins" in source
    assert "file_plugin_loader" in source or "level_0_infra.level_0" in source
