"""
Canonical pipeline factories for release workflows.

``ReleasePipelineFactory`` in ``level_3.release_pipelines.factory`` delegates
here; add or change release steps in this module only.
"""

from pathlib import Path
from typing import Callable

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    build_python_package,
    build_docs, 
    deploy_docs,
    run_python_package_tests,
    upload_to_pypi
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    validate_python_package,
    PipelineStep,
    StepPipelineEngine,
    create_git_tag, 
    push_to_remote,
    check_git_status
)

StepCallable = Callable[..., None]


def _wrap(step_func: StepCallable, *, version: str, dry_run: bool, root: Path) -> StepCallable:
    def wrapped(**kwargs):
        return step_func(version=version, dry_run=dry_run, repo_root=root, package_root=root, docs_root=root, **kwargs)

    return wrapped


def _wrap_python_build(*, root: Path) -> StepCallable:
    def wrapped(**kwargs):
        package_root = Path(kwargs["package_root"]) if kwargs.get("package_root") else root
        return build_python_package(package_root)

    return wrapped


def _wrap_python_tests(*, root: Path) -> StepCallable:
    def wrapped(**kwargs):
        package_root = Path(kwargs["package_root"]) if kwargs.get("package_root") else root
        return run_python_package_tests(package_root)

    return wrapped


def _wrap_python_validate(*, root: Path) -> StepCallable:
    def wrapped(**kwargs):
        package_root = Path(kwargs["package_root"]) if kwargs.get("package_root") else root
        return validate_python_package(package_root)

    return wrapped


def create_python_package_pipeline(*, config, version: str, dry_run: bool, root: Path) -> StepPipelineEngine:
    pipeline = StepPipelineEngine(config, "Python Package Release")

    pipeline.add_step(
        PipelineStep(
            name="validate_package",
            log_filename="validation.log",
            qc_func=_wrap_python_validate(root=root),
            input_key="package_root",
            run_mode="global",
        )
    )
    pipeline.add_step(
        PipelineStep(
            name="run_tests",
            log_filename="tests.log",
            qc_func=_wrap_python_tests(root=root),
            input_key="package_root",
            run_mode="global",
        )
    )
    pipeline.add_step(
        PipelineStep(
            name="build_package",
            log_filename="build.log",
            qc_func=_wrap_python_build(root=root),
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


def create_git_repo_pipeline(*, config, version: str, dry_run: bool, root: Path) -> StepPipelineEngine:
    pipeline = StepPipelineEngine(config, "Git Repository Release")

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


def create_docs_pipeline(*, config, version: str, dry_run: bool, root: Path) -> StepPipelineEngine:
    pipeline = StepPipelineEngine(config, "Documentation Release")

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


def create_full_pipeline(*, config, version: str, dry_run: bool, root: Path) -> StepPipelineEngine:
    pipeline = StepPipelineEngine(config, "Full Release")

    for step in create_python_package_pipeline(config=config, version=version, dry_run=dry_run, root=root).steps:
        pipeline.add_step(step)
    for step in create_git_repo_pipeline(config=config, version=version, dry_run=dry_run, root=root).steps:
        pipeline.add_step(step)
    for step in create_docs_pipeline(config=config, version=version, dry_run=dry_run, root=root).steps:
        pipeline.add_step(step)

    return pipeline

