"""Release pipeline factory delegates to canonical generic_release_tool builders."""

from __future__ import annotations

from pathlib import Path

import pytest

_FACTORY_PATH = (
    Path(__file__).resolve().parents[3]
    / "layer_1_tools"
    / "level_0_infra"
    / "level_3"
    / "release_pipelines"
    / "factory.py"
)


def test_factory_module_delegates_to_canonical_builders() -> None:
    source = _FACTORY_PATH.read_text(encoding="utf-8")
    assert "generic_release_tool.pipelines import" in source
    assert "return create_python_package_pipeline(" in source
    assert "return create_git_repo_pipeline(" in source
    assert "return create_docs_pipeline(" in source
    assert "return create_full_pipeline(" in source
    assert "_validate_package_step" not in source


def _step_snapshot(pipeline) -> list[tuple[str, str, str, str]]:
    return [(s.name, s.log_filename, s.input_key, s.run_mode) for s in pipeline.steps]


@pytest.fixture
def release_params(tmp_path: Path) -> dict:
    pytest.importorskip("torchvision")
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.root_schema import Config

    config = Config()
    config.workspace.domains = ["default"]
    config.domains = config.workspace.domains
    return {
        "config": config,
        "version": "1.2.3",
        "dry_run": True,
        "root": tmp_path,
    }


@pytest.mark.parametrize(
    ("factory_method_name", "canonical_builder_name"),
    [
        ("create_python_package_pipeline", "create_python_package_pipeline"),
        ("create_git_release_pipeline", "create_git_repo_pipeline"),
        ("create_documentation_pipeline", "create_docs_pipeline"),
        ("create_full_release_pipeline", "create_full_pipeline"),
    ],
)
def test_factory_matches_canonical_step_graph(
    factory_method_name: str,
    canonical_builder_name: str,
    release_params,
) -> None:
    pytest.importorskip("torchvision")
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import generic_release_tool
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_3.release_pipelines.factory import (
        ReleasePipelineFactory,
    )

    factory_method = getattr(ReleasePipelineFactory, factory_method_name)
    canonical_builder = getattr(generic_release_tool.pipelines, canonical_builder_name)
    factory_pipeline = factory_method(**release_params)
    canonical_pipeline = canonical_builder(**release_params)

    assert factory_pipeline.name == canonical_pipeline.name
    assert _step_snapshot(factory_pipeline) == _step_snapshot(canonical_pipeline)


def test_python_package_pipeline_step_order(release_params) -> None:
    pytest.importorskip("torchvision")
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_3.release_pipelines.factory import (
        ReleasePipelineFactory,
    )

    pipeline = ReleasePipelineFactory.create_python_package_pipeline(**release_params)
    assert [s.name for s in pipeline.steps] == [
        "validate_package",
        "run_tests",
        "build_package",
        "upload_pypi",
    ]
