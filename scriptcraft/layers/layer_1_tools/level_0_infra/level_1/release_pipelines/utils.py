# release_pipelines/utils.py

from layers.layer_1_tools.level_0_infra.level_0.release_pipelines.context import ReleasePipelineContext


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