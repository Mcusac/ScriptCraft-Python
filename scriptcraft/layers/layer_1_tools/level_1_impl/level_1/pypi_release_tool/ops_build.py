import shutil
from pathlib import Path

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print

from layers.layer_1_tools.level_1_impl.level_0.subprocess.runner import (
    run,
    python_module_args,
    stringify_args,
)


def clean_build_artifacts() -> None:
    for folder in ["build", "dist"]:
        p = Path(folder)
        if p.exists() and p.is_dir():
            shutil.rmtree(p)

    for egg_info in Path(".").glob("*.egg-info"):
        if egg_info.is_dir():
            shutil.rmtree(egg_info)
        else:
            egg_info.unlink(missing_ok=True)


def build_package() -> bool:
    log_and_print("🔨 Building package...")

    clean_build_artifacts()

    args = python_module_args("build")

    result = run(args)

    if not result.ok:
        log_and_print(
            f"❌ Package build failed ({stringify_args(args)})",
            level="error",
        )
        if result.stderr:
            log_and_print(result.stderr, level="error")
        return False

    log_and_print("✅ Package built successfully")
    return True