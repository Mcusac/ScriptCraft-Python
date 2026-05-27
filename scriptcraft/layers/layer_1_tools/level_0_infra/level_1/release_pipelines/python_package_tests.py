import subprocess
import sys

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print


def run_python_package_tests(package_root: Path) -> bool:
    log_and_print("🧪 Running tests...")

    tests_dir = package_root / "tests"
    if not tests_dir.exists():
        log_and_print("⚠️ No tests directory found, skipping tests", level="warning")
        return True

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(package_root),
        )
        if result.returncode != 0:
            stderr = (result.stderr or "").strip()
            log_and_print(
                f"❌ Tests failed: {stderr or 'unknown test error'}",
                level="error",
            )
            return False
    except FileNotFoundError:
        test_files = list(tests_dir.glob("test_*.py"))
        for test_file in test_files:
            log_and_print(f"Running {test_file}...")
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=str(package_root),
            )
            if result.returncode != 0:
                stderr = (result.stderr or "").strip()
                log_and_print(
                    f"❌ {test_file} failed: {stderr or 'unknown test error'}",
                    level="error",
                )
                return False

    log_and_print("✅ All tests passed")
    return True
