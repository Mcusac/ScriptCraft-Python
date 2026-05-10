import shutil
import subprocess
import sys

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1.release_pipelines.utils import build_context


def validate_package(**kwargs) -> None:
    ctx = build_context(**kwargs)

    log_and_print("🔍 Validating package...")

    for file in ["pyproject.toml", "README.md"]:
        if not Path(file).exists():
            log_and_print(f"❌ Missing required file: {file}", level="error")
            return

    if Path("tests").exists():
        log_and_print("🧪 Running validation tests...")
        result = subprocess.run([sys.executable, "tests/test_package_integrity.py"],
                                capture_output=True, text=True)
        if result.returncode != 0:
            log_and_print(f"❌ Validation tests failed: {result.stderr}", level="error")
            return

    log_and_print("✅ Package validation passed")


def run_tests(**kwargs) -> None:
    log_and_print("🧪 Running tests...")

    if not Path("tests").exists():
        log_and_print("⚠️ No tests directory found, skipping tests")
        return

    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"],
                                capture_output=True, text=True)

        if result.returncode != 0:
            log_and_print(f"❌ Tests failed: {result.stderr}", level="error")
            return

    except FileNotFoundError:
        test_files = list(Path("tests").glob("test_*.py"))

        for test_file in test_files:
            log_and_print(f"Running {test_file}...")
            result = subprocess.run([sys.executable, str(test_file)],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                log_and_print(f"❌ {test_file} failed: {result.stderr}", level="error")
                return

    log_and_print("✅ All tests passed")


def build_package(**kwargs) -> None:
    log_and_print("🔨 Building package...")

    for artifact in ["build", "dist", "*.egg-info"]:
        path = Path(artifact)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    result = subprocess.run([sys.executable, "-m", "build"],
                            capture_output=True, text=True)

    if result.returncode != 0:
        log_and_print(f"❌ Build failed: {result.stderr}", level="error")
        return

    log_and_print("✅ Package built successfully")


def upload_to_pypi(**kwargs) -> None:
    ctx = build_context(**kwargs)

    log_and_print("📦 Uploading to PyPI...")

    if ctx.dry_run:
        log_and_print("🔍 DRY RUN: Would upload to PyPI")
        return

    try:
        result = subprocess.run([sys.executable, "-m", "twine", "upload", "dist/*"],
                                capture_output=True, text=True)

        if result.returncode != 0:
            log_and_print(f"❌ Upload failed: {result.stderr}", level="error")
            return

    except FileNotFoundError:
        log_and_print("❌ twine not found. Install with: pip install twine", level="error")
        return

    log_and_print("✅ Package uploaded to PyPI")