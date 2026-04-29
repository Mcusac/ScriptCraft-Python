from __future__ import annotations

from pathlib import Path

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print

from .ops_build import build_package
from .runner import python_module_args, run_command, stringify_args


def _dist_files() -> list[str]:
    dist = Path("dist")
    if not dist.exists():
        return []
    return [str(p) for p in sorted(dist.glob("*")) if p.is_file()]


def upload_testpypi() -> bool:
    log_and_print("🧪 Testing PyPI upload...")

    if not build_package():
        return False

    files = _dist_files()
    if not files:
        log_and_print("❌ No dist/* files found to upload", level="error")
        return False

    args = python_module_args("twine", "upload", "--repository", "testpypi", *files)
    result = run_command(args, description=f"Testing upload to PyPI test ({stringify_args(args)})")
    if result.returncode != 0:
        log_and_print("❌ Test upload failed", level="error")
        if result.stderr:
            log_and_print(result.stderr, level="error")
        return False

    log_and_print("✅ Test upload successful")
    return True


def upload_pypi() -> bool:
    log_and_print("📦 Releasing to PyPI...")

    if not build_package():
        return False

    files = _dist_files()
    if not files:
        log_and_print("❌ No dist/* files found to upload", level="error")
        return False

    args = python_module_args("twine", "upload", *files)
    result = run_command(args, description=f"Uploading to PyPI ({stringify_args(args)})")
    if result.returncode != 0:
        log_and_print("❌ Release upload failed", level="error")
        if result.stderr:
            log_and_print(result.stderr, level="error")
        return False

    log_and_print("✅ Release upload successful")
    return True

