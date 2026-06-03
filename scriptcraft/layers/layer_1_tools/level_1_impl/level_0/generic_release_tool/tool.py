"""
Generic Release Tool core class.

Canonical for standalone repo releases via infra pipeline factories
(validate, build, upload, tag). Workspace-integrated python-package releases
should use release_manager ``python_package`` mode (L2), which shares L0
mechanics under ``level_0/release_manager/``.

Tool placement: level_4 (imports infra level_4 pipeline factories).
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    detect_repo_root, 
    resolve_version,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    create_docs_pipeline,
    create_full_pipeline,
    create_git_repo_pipeline,
    create_python_package_pipeline,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool


@dataclass(frozen=True)
class ReleaseContext:
    version: str
    dry_run: bool
    timestamp: str
    repo_root: Path


PipelineFactory = Callable[[ReleaseContext], object]


class GenericReleaseTool(BaseTool):
    """Standalone release tool using infra pipeline factories (not workspace submodule sync)."""

    def __init__(self):
        super().__init__(
            name="Generic Release Tool",
            description="🚀 Workspace-agnostic release management using pipelines",
            tool_name="generic_release_tool",
        )
        self._pipeline_factories: Dict[str, Callable[[ReleaseContext], object]] = {}
        self._setup_default_pipelines()

    def _setup_default_pipelines(self) -> None:
        self._pipeline_factories = {
            "python_package": lambda ctx: create_python_package_pipeline(
                config=self.config,
                version=ctx.version,
                dry_run=ctx.dry_run,
                root=ctx.repo_root,
            ),
            "git_repo": lambda ctx: create_git_repo_pipeline(
                config=self.config,
                version=ctx.version,
                dry_run=ctx.dry_run,
                root=ctx.repo_root,
            ),
            "docs": lambda ctx: create_docs_pipeline(
                config=self.config,
                version=ctx.version,
                dry_run=ctx.dry_run,
                root=ctx.repo_root,
            ),
            "full": lambda ctx: create_full_pipeline(
                config=self.config,
                version=ctx.version,
                dry_run=ctx.dry_run,
                root=ctx.repo_root,
            ),
        }

    def run(
        self,
        pipeline: Optional[str] = None,
        version: Optional[str] = None,
        dry_run: bool = False,
        **_: object,
    ) -> None:
        """Run a release pipeline."""
        pipeline_name = pipeline or "python_package"
        if pipeline_name not in self._pipeline_factories:
            log_and_print(f"❌ Unknown pipeline: {pipeline_name}", level="error")
            log_and_print(f"Available pipelines: {list(self._pipeline_factories.keys())}")
            return

        repo_root = detect_repo_root(start=Path.cwd()) or Path.cwd()

        resolved = resolve_version(repo_root=repo_root)
        effective_version = version or resolved.version

        ctx = ReleaseContext(
            version=effective_version,
            dry_run=dry_run,
            timestamp=datetime.now().isoformat(),
            repo_root=repo_root,
        )

        log_and_print(f"🚀 Starting {pipeline_name} release pipeline...")
        log_and_print(f"📌 Repo root: {ctx.repo_root}")
        log_and_print(f"🏷️ Version: {ctx.version} (source: {resolved.source})")

        if dry_run:
            log_and_print("🔍 DRY RUN MODE - No actual changes will be made")

        release_pipeline = self._pipeline_factories[pipeline_name](ctx)
        release_pipeline.run()

        log_and_print(f"✅ {pipeline_name} release pipeline completed!")

