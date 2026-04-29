
from typing import Callable

from layers.layer_1_pypi.level_0_infra.level_6.base_tool import BaseTool
from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_pypi.level_1_impl.level_2.git_submodule_tool.operations import pull_submodules, push_submodules, sync_submodules, update_submodules


class GitSubmoduleTool(BaseTool):
    """Tool for Git submodule operations."""

    def __init__(self) -> None:
        super().__init__(
            name="Git Submodule Tool",
            description="Handles Git submodule operations",
        )

        self._operations: dict[str, Callable[[], bool]] = {
            "sync": sync_submodules,
            "push": push_submodules,
            "pull": pull_submodules,
            "update": update_submodules,
        }

    def run(self, operation: str = "sync", **kwargs) -> bool:  # noqa: ARG002 - forward-compatible
        op = self._operations.get(operation)
        if not op:
            log_and_print(f"❌ Unknown operation: {operation}", level="error")
            return False
        return op()

