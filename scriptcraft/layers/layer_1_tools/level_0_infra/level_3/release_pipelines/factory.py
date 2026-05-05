from typing import Any

from layers.layer_1_tools.level_0_infra.level_0.release_pipelines.context import ReleasePipelineContext
from layers.layer_1_tools.level_0_infra.level_0.release_pipelines.run_modes import RunMode
from layers.layer_1_tools.level_0_infra.level_2.root_schema import Config
from layers.layer_1_tools.level_0_infra.level_2.pipeline_base import BasePipeline, PipelineStep
from layers.layer_1_tools.level_0_infra.level_2.release_pipelines.steps_python import validate_package, run_tests, build_package, upload_to_pypi
from layers.layer_1_tools.level_0_infra.level_2.release_pipelines.steps_git import check_git_status, create_git_tag, push_to_remote
from layers.layer_1_tools.level_0_infra.level_2.release_pipelines.steps_docs import build_docs, deploy_docs


class ReleasePipelineFactory:
    """Factory for creating release pipelines."""

    @staticmethod
    def build_context(**kwargs) -> ReleasePipelineContext:
        return ReleasePipelineContext(
            version=kwargs.get("version", "0.0.0"),
            dry_run=kwargs.get("dry_run", False),
            repo_root=kwargs.get("repo_root"),
            package_root=kwargs.get("package_root"),
            docs_root=kwargs.get("docs_root"),
            timestamp=kwargs.get("timestamp"),
            extras=kwargs,
        )

    @staticmethod
    def create_python_package_pipeline(config: Any = None) -> BasePipeline:
        config = config or Config()
        config.workspace.domains = ["default"]

        pipeline = BasePipeline(config, "Python Package Release")

        pipeline.add_step(PipelineStep("validate_package", "validation.log", validate_package, "package_root", RunMode.GLOBAL.value))
        pipeline.add_step(PipelineStep("run_tests", "tests.log", run_tests, "package_root", RunMode.GLOBAL.value))
        pipeline.add_step(PipelineStep("build_package", "build.log", build_package, "package_root", RunMode.GLOBAL.value))
        pipeline.add_step(PipelineStep("upload_pypi", "upload.log", upload_to_pypi, "package_root", RunMode.GLOBAL.value))

        return pipeline

    @staticmethod
    def create_git_release_pipeline(config: Any = None) -> BasePipeline:
        config = config or Config()
        config.workspace.domains = ["default"]

        pipeline = BasePipeline(config, "Git Repository Release")

        pipeline.add_step(PipelineStep("check_git_status", "git_status.log", check_git_status, "repo_root", RunMode.GLOBAL.value))
        pipeline.add_step(PipelineStep("create_tag", "tag.log", create_git_tag, "repo_root", RunMode.GLOBAL.value))
        pipeline.add_step(PipelineStep("push_to_remote", "push.log", push_to_remote, "repo_root", RunMode.GLOBAL.value))

        return pipeline

    @staticmethod
    def create_documentation_pipeline(config: Any = None) -> BasePipeline:
        config = config or Config()
        config.workspace.domains = ["default"]

        pipeline = BasePipeline(config, "Documentation Release")

        pipeline.add_step(PipelineStep("build_docs", "docs_build.log", build_docs, "docs_root", RunMode.GLOBAL.value))
        pipeline.add_step(PipelineStep("deploy_docs", "docs_deploy.log", deploy_docs, "docs_root", RunMode.GLOBAL.value))

        return pipeline

    @staticmethod
    def create_full_release_pipeline(config: Any = None) -> BasePipeline:
        config = config or Config()
        config.workspace.domains = ["default"]

        pipeline = BasePipeline(config, "Full Release")

        for step in ReleasePipelineFactory.create_python_package_pipeline(config).steps:
            pipeline.add_step(step)

        for step in ReleasePipelineFactory.create_git_release_pipeline(config).steps:
            pipeline.add_step(step)

        for step in ReleasePipelineFactory.create_documentation_pipeline(config).steps:
            pipeline.add_step(step)

        return pipeline