
from typing import Callable

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_tools.level_1_impl.level_0.git_workspace_tool.operations import check_status, commit_changes, create_tag, pull_workspace, push_workspace
from layers.layer_1_tools.level_1_impl.level_0.subprocess.runner import run_ok
from layers.layer_1_tools.level_1_impl.level_1.git.probes import (
    is_git_repo,
    porcelain_status_has_changes,
)


class GitWorkspaceTool(BaseTool):
    """Tool for Git workspace operations."""

    def __init__(self) -> None:
        super().__init__(
            name="Git Workspace Tool",
            description="Handles Git workspace operations",
        )

        self._operations: dict[str, Callable[..., bool]] = {
            "push": lambda **_: push_workspace(
                is_git_repo=is_git_repo,
                porcelain_status_has_changes=porcelain_status_has_changes,
                run_ok=run_ok,
            ),
            "pull": lambda **_: pull_workspace(
                is_git_repo=is_git_repo,
                run_ok=run_ok,
            ),
            "status": lambda **_: check_status(
                is_git_repo=is_git_repo,
                porcelain_status_has_changes=porcelain_status_has_changes,
            ),
            "commit": lambda *, message=None, **__: commit_changes(
                is_git_repo=is_git_repo,
                porcelain_status_has_changes=porcelain_status_has_changes,
                run_ok=run_ok,
                message=message,
            ),
            "tag": lambda *, version=None, **__: create_tag(
                is_git_repo=is_git_repo,
                run_ok=run_ok,
                version=version,
            ),
        }

    def run(self, operation: str = "push", **kwargs) -> bool:
        log_and_print(f"🚀 Starting Git workspace {operation} operation...")

        op = self._operations.get(operation)
        if not op:
            log_and_print(f"❌ Unknown operation: {operation}", level="error")
            return False

        return op(**kwargs)

