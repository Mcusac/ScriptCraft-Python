"""Workspace release mode entrypoint for Release Manager."""

from pathlib import Path
from typing import List, Optional

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    WorkspaceReleaseContext,
    WorkspaceReleasePipeline,
)


def workspace_release_mode(
    input_paths: List[Path],
    output_dir: Path,
    domain: Optional[str] = None,
    version_type: Optional[str] = None,
    auto_push: bool = False,
    force: bool = False,
    custom_message: Optional[str] = None,
    **kwargs,
) -> None:
    _ = kwargs
    ctx = WorkspaceReleaseContext(
        input_paths=input_paths,
        output_dir=output_dir,
        domain=domain,
        version_type=version_type,
        auto_push=auto_push,
        force=force,
        custom_message=custom_message,
    )
    WorkspaceReleasePipeline(ctx).run()
