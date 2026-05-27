from typing import Literal
from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    build_python_package,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    validate_python_package,
    upload_pypi, 
    upload_testpypi
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool

_Operation = Literal["test", "release", "validate", "build"]


class PyPIReleaseTool(BaseTool):
    """Tool for PyPI testing and release operations."""

    def __init__(self) -> None:
        super().__init__(
            name="PyPI Release Tool",
            description="Handles PyPI testing and release operations",
        )

    def run(self, operation: _Operation = "test", **kwargs) -> bool:
        log_and_print(f"🚀 Starting PyPI {operation} operation...")

        if operation == "test":
            ok = upload_testpypi()
        elif operation == "release":
            ok = upload_pypi()
        elif operation == "validate":
            ok = validate_python_package(Path("."))
        elif operation == "build":
            ok = build_python_package(Path("."))
        else:
            log_and_print(f"❌ Unknown operation: {operation}", level="error")
            ok = False

        if ok:
            self.logger.info("Operation '%s' succeeded", operation)
        else:
            self.logger.error("Operation '%s' failed", operation)
        return ok

