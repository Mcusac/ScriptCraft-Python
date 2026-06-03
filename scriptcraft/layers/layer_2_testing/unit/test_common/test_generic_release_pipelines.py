"""Release pipeline builders exposed via the level_4 barrel."""

from __future__ import annotations

from pathlib import Path

import pytest


def _step_snapshot(pipeline) -> list[tuple[str, str, str, str]]:
    return [(s.name, s.log_filename, s.input_key, s.run_mode) for s in pipeline.steps]


@pytest.fixture
def release_params(tmp_path: Path) -> dict:
    pytest.importorskip("torchvision")
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import Config

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
    "builder_name",
    [
        "create_python_package_pipeline",
        "create_git_repo_pipeline",
        "create_docs_pipeline",
        "create_full_pipeline",
    ],
)
def test_level4_barrel_exposes_release_pipeline_builders(
    builder_name: str,
) -> None:
    from scriptcraft.layers.layer_1_tools.level_0_infra import level_4

    assert hasattr(level_4, builder_name)


@pytest.mark.parametrize(
    "builder_name",
    [
        "create_python_package_pipeline",
        "create_git_repo_pipeline",
        "create_docs_pipeline",
        "create_full_pipeline",
    ],
)
def test_release_pipeline_builders_produce_named_pipelines(
    builder_name: str,
    release_params,
) -> None:
    pytest.importorskip("torchvision")
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
        create_docs_pipeline,
        create_full_pipeline,
        create_git_repo_pipeline,
        create_python_package_pipeline,
    )

    builders = {
        "create_python_package_pipeline": create_python_package_pipeline,
        "create_git_repo_pipeline": create_git_repo_pipeline,
        "create_docs_pipeline": create_docs_pipeline,
        "create_full_pipeline": create_full_pipeline,
    }
    pipeline = builders[builder_name](**release_params)
    assert pipeline.name
    assert pipeline.steps


def test_python_package_pipeline_step_order(release_params) -> None:
    pytest.importorskip("torchvision")
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
        create_python_package_pipeline,
    )

    pipeline = create_python_package_pipeline(**release_params)
    assert [s.name for s in pipeline.steps] == [
        "validate_package",
        "run_tests",
        "build_package",
        "upload_pypi",
    ]


def test_full_pipeline_composes_child_step_graphs(release_params) -> None:
    pytest.importorskip("torchvision")
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
        create_full_pipeline,
        create_python_package_pipeline,
    )

    full_pipeline = create_full_pipeline(**release_params)
    package_pipeline = create_python_package_pipeline(**release_params)
    assert _step_snapshot(full_pipeline)[: len(package_pipeline.steps)] == _step_snapshot(
        package_pipeline
    )
