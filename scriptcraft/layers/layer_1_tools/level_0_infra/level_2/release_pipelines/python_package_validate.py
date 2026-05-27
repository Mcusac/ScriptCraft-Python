from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    python_file_args,
    run,
)

_REQUIRED_PACKAGE_FILES = ("pyproject.toml", "README.md")


def validate_python_package(package_root: Path) -> bool:
    log_and_print("🔍 Validating package...")

    for filename in _REQUIRED_PACKAGE_FILES:
        if not (package_root / filename).exists():
            log_and_print(f"❌ Missing required file: {filename}", level="error")
            return False

    integrity_test = package_root / "tests" / "test_package_integrity.py"
    if not integrity_test.exists():
        log_and_print("✅ Package validation passed")
        return True

    log_and_print("🧪 Running validation tests...")
    result = run(python_file_args(str(integrity_test)), cwd=package_root)
    if not result.ok:
        log_and_print(
            f"❌ Validation tests failed: {integrity_test.name}",
            level="error",
        )
        if result.stderr:
            log_and_print(result.stderr, level="error")
        return False

    log_and_print("✅ Package validation passed")
    return True
