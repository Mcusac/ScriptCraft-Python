from __future__ import annotations

from typing import Literal

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from .ops_build import build_package
from .ops_upload import upload_pypi, upload_testpypi
from .ops_validate import validate_package


Operation = Literal["test", "release", "validate", "build"]


class PyPIReleaseTool(BaseTool):
    """Tool for PyPI testing and release operations."""

    def __init__(self) -> None:
        super().__init__(
            name="PyPI Release Tool",
            description="Handles PyPI testing and release operations",
        )

    def run(self, operation: Operation = "test", **kwargs) -> bool:
        log_and_print(f"🚀 Starting PyPI {operation} operation...")

        if operation == "test":
            ok = upload_testpypi()
        elif operation == "release":
            ok = upload_pypi()
        elif operation == "validate":
            ok = validate_package()
        elif operation == "build":
            ok = build_package()
        else:
            log_and_print(f"❌ Unknown operation: {operation}", level="error")
            ok = False

        if ok:
            self.logger.info("Operation '%s' succeeded", operation)
        else:
            self.logger.error("Operation '%s' failed", operation)
        return ok

