from pathlib import Path

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.subprocess.runner import (
    run,
    python_module_args,
    stringify_args,
)

from .ops_build import build_package


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

    result = run(args)

    if not result.ok:
        log_and_print(
            f"❌ Test upload failed ({stringify_args(args)})",
            level="error",
        )
        if result.stderr:
            log_and_print(result.stderr, level="error")
        return False

    log_and_print("✅ Test PyPI upload successful")
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

    result = run(args)

    if not result.ok:
        log_and_print(
            f"❌ Release upload failed ({stringify_args(args)})",
            level="error",
        )
        if result.stderr:
            log_and_print(result.stderr, level="error")
        return False

    log_and_print("✅ Release upload successful")
    return True