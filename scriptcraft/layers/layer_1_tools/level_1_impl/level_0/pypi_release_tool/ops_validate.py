from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1.subprocess.runner import (
    run,
    python_file_args,
)


def validate_package() -> bool:
    log_and_print("🔍 Validating package...")

    # ---- static checks ----
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

    # ---- dynamic test execution ----
    log_and_print("🧪 Running validation tests...")

    for test_file in test_files:
        args = python_file_args(str(test_file))

        result = run(args)

        if not result.ok:
            log_and_print(
                f"❌ Validation test failed: {test_file}",
                level="error",
            )
            if result.stderr:
                log_and_print(result.stderr, level="error")
            return False

    log_and_print("✅ Package validation passed")
    return True