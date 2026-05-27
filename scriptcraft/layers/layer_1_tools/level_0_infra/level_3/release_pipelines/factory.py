"""
Compatibility facade for release pipeline construction.

Canonical step graphs live in
``level_3.generic_release_tool.pipelines``; this module delegates there so
CLI and legacy callers keep ``ReleasePipelineFactory`` without duplicating
pipeline assembly.
"""

from pathlib import Path
from typing import Any, Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.generic_release_tool.version_resolver import (
    detect_repo_root,
    resolve_version,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.pipeline_base import StepPipelineEngine
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.root_schema import Config
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3.generic_release_tool.pipelines import (
    create_docs_pipeline,
    create_full_pipeline,
    create_git_repo_pipeline,
    create_python_package_pipeline,
)


def _prepare_config(config: Any = None) -> Config:
    """Normalize config for pipeline engines (domains required)."""
    prepared = config if config is not None else Config()
    prepared.workspace.domains = ["default"]
    prepared.domains = prepared.workspace.domains
    return prepared


def _resolve_release_context(
    *,
    config: Any = None,
    version: Optional[str] = None,
    dry_run: bool = False,
    root: Optional[Path] = None,
) -> tuple[Config, str, bool, Path]:
    prepared = _prepare_config(config)
    effective_root = root or detect_repo_root(start=Path.cwd()) or Path.cwd()
    if version is None:
        resolved = resolve_version(repo_root=effective_root)
        version = resolved.version
    return prepared, version, dry_run, effective_root


class ReleasePipelineFactory:
    """Delegates to generic_release_tool pipeline builders (single source of truth)."""

    @staticmethod
    def create_python_package_pipeline(
        config: Any = None,
        *,
        version: Optional[str] = None,
        dry_run: bool = False,
        root: Optional[Path] = None,
    ) -> StepPipelineEngine:
        prepared, effective_version, effective_dry_run, effective_root = _resolve_release_context(
            config=config,
            version=version,
            dry_run=dry_run,
            root=root,
        )
        return create_python_package_pipeline(
            config=prepared,
            version=effective_version,
            dry_run=effective_dry_run,
            root=effective_root,
        )

    @staticmethod
    def create_git_release_pipeline(
        config: Any = None,
        *,
        version: Optional[str] = None,
        dry_run: bool = False,
        root: Optional[Path] = None,
    ) -> StepPipelineEngine:
        prepared, effective_version, effective_dry_run, effective_root = _resolve_release_context(
            config=config,
            version=version,
            dry_run=dry_run,
            root=root,
        )
        return create_git_repo_pipeline(
            config=prepared,
            version=effective_version,
            dry_run=effective_dry_run,
            root=effective_root,
        )

    @staticmethod
    def create_documentation_pipeline(
        config: Any = None,
        *,
        version: Optional[str] = None,
        dry_run: bool = False,
        root: Optional[Path] = None,
    ) -> StepPipelineEngine:
        prepared, effective_version, effective_dry_run, effective_root = _resolve_release_context(
            config=config,
            version=version,
            dry_run=dry_run,
            root=root,
        )
        return create_docs_pipeline(
            config=prepared,
            version=effective_version,
            dry_run=effective_dry_run,
            root=effective_root,
        )

    @staticmethod
    def create_full_release_pipeline(
        config: Any = None,
        *,
        version: Optional[str] = None,
        dry_run: bool = False,
        root: Optional[Path] = None,
    ) -> StepPipelineEngine:
        prepared, effective_version, effective_dry_run, effective_root = _resolve_release_context(
            config=config,
            version=version,
            dry_run=dry_run,
            root=root,
        )
        return create_full_pipeline(
            config=prepared,
            version=effective_version,
            dry_run=effective_dry_run,
            root=effective_root,
        )
