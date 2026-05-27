
from typing import Callable

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    is_git_repo,
    porcelain_status_has_changes,
    check_status,
    commit_changes,
    create_tag,
    pull_workspace,
    push_workspace,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool


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
            ),
            "pull": lambda **_: pull_workspace(
                is_git_repo=is_git_repo,
            ),
            "status": lambda **_: check_status(
                is_git_repo=is_git_repo,
                porcelain_status_has_changes=porcelain_status_has_changes,
            ),
            "commit": lambda *, message=None, **__: commit_changes(
                is_git_repo=is_git_repo,
                porcelain_status_has_changes=porcelain_status_has_changes,
                message=message,
            ),
            "tag": lambda *, version=None, **__: create_tag(
                is_git_repo=is_git_repo,
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

