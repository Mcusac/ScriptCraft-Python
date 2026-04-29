from __future__ import annotations

from pathlib import Path

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print

from .runner import python_file_args, run_command, stringify_args


def validate_package() -> bool:
    log_and_print("🔍 Validating package...")

    for required in ["pyproject.toml", "README.md"]:
        if not Path(required).exists():
            log_and_print(f"❌ Missing required file: {required}", level="error")
            return False

    tests_dir = Path("tests")
    if not tests_dir.exists():
        log_and_print("✅ Package validation passed")
        return True

    test_files = sorted(tests_dir.glob("test_*.py"))
    if not test_files:
        log_and_print("✅ Package validation passed")
        return True

    log_and_print("🧪 Running validation tests...")
    for test_file in test_files:
        args = python_file_args(str(test_file))
        result = run_command(args, description=f"Running {test_file} ({stringify_args(args)})")
        if result.returncode != 0:
            log_and_print(f"❌ Validation test failed: {test_file}", level="error")
            if result.stderr:
                log_and_print(result.stderr, level="error")
            return False

    log_and_print("✅ Package validation passed")
    return True

