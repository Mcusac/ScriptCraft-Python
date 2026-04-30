"""
Pipeline factories for the Generic Release Tool.
"""

from pathlib import Path
from typing import Callable

from layers.layer_1_tools.level_0_infra.level_2.pipeline_base import BasePipeline, PipelineStep

from layers.layer_1_tools.level_1_impl.level_0.generic_release_tool.steps_docs import build_docs, deploy_docs
from layers.layer_1_tools.level_1_impl.level_0.generic_release_tool.steps_git import check_git_status, create_git_tag, push_to_remote
from layers.layer_1_tools.level_1_impl.level_0.generic_release_tool.steps_python_package import build_package, run_tests, upload_to_pypi, validate_package


StepCallable = Callable[..., None]


def _wrap(step_func: StepCallable, *, version: str, dry_run: bool, root: Path) -> StepCallable:
    def wrapped(**kwargs):
        return step_func(version=version, dry_run=dry_run, repo_root=root, package_root=root, docs_root=root, **kwargs)

    return wrapped


def create_python_package_pipeline(*, config, version: str, dry_run: bool, root: Path) -> BasePipeline:
    pipeline = BasePipeline(config, "Python Package Release")

    pipeline.add_step(
        PipelineStep(
            name="validate_package",
            log_filename="validation.log",
            qc_func=_wrap(validate_package, version=version, dry_run=dry_run, root=root),
            input_key="package_root",
            run_mode="global",
        )
    )
    pipeline.add_step(
        PipelineStep(
            name="run_tests",
            log_filename="tests.log",
            qc_func=_wrap(run_tests, version=version, dry_run=dry_run, root=root),
            input_key="package_root",
            run_mode="global",
        )
    )
    pipeline.add_step(
        PipelineStep(
            name="build_package",
            log_filename="build.log",
            qc_func=_wrap(build_package, version=version, dry_run=dry_run, root=root),
            input_key="package_root",
            run_mode="global",
        )
    )
    pipeline.add_step(
        PipelineStep(
            name="upload_pypi",
            log_filename="upload.log",
            qc_func=_wrap(upload_to_pypi, version=version, dry_run=dry_run, root=root),
            input_key="package_root",
            run_mode="global",
        )
    )

    return pipeline


def create_git_repo_pipeline(*, config, version: str, dry_run: bool, root: Path) -> BasePipeline:
    pipeline = BasePipeline(config, "Git Repository Release")

    pipeline.add_step(
        PipelineStep(
            name="check_git_status",
            log_filename="git_status.log",
            qc_func=_wrap(check_git_status, version=version, dry_run=dry_run, root=root),
            input_key="repo_root",
            run_mode="global",
        )
    )
    pipeline.add_step(
        PipelineStep(
            name="create_tag",
            log_filename="tag.log",
            qc_func=_wrap(create_git_tag, version=version, dry_run=dry_run, root=root),
            input_key="repo_root",
            run_mode="global",
        )
    )
    pipeline.add_step(
        PipelineStep(
            name="push_to_remote",
            log_filename="push.log",
            qc_func=_wrap(push_to_remote, version=version, dry_run=dry_run, root=root),
            input_key="repo_root",
            run_mode="global",
        )
    )

    return pipeline


def create_docs_pipeline(*, config, version: str, dry_run: bool, root: Path) -> BasePipeline:
    pipeline = BasePipeline(config, "Documentation Release")

    pipeline.add_step(
        PipelineStep(
            name="build_docs",
            log_filename="docs_build.log",
            qc_func=_wrap(build_docs, version=version, dry_run=dry_run, root=root),
            input_key="docs_root",
            run_mode="global",
        )
    )
    pipeline.add_step(
        PipelineStep(
            name="deploy_docs",
            log_filename="docs_deploy.log",
            qc_func=_wrap(deploy_docs, version=version, dry_run=dry_run, root=root),
            input_key="docs_root",
            run_mode="global",
        )
    )

    return pipeline


def create_full_pipeline(*, config, version: str, dry_run: bool, root: Path) -> BasePipeline:
    pipeline = BasePipeline(config, "Full Release")

    for step in create_python_package_pipeline(config=config, version=version, dry_run=dry_run, root=root).steps:
        pipeline.add_step(step)
    for step in create_git_repo_pipeline(config=config, version=version, dry_run=dry_run, root=root).steps:
        pipeline.add_step(step)
    for step in create_docs_pipeline(config=config, version=version, dry_run=dry_run, root=root).steps:
        pipeline.add_step(step)

    return pipeline

