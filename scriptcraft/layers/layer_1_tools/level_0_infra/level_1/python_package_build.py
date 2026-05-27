import shutil
import subprocess
import sys

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print


def clean_python_build_artifacts(package_root: Path) -> None:
    log_and_print("🧹 Cleaning build artifacts...")

    for artifact_name in ("build", "dist"):
        artifact_path = package_root / artifact_name
        if not artifact_path.exists():
            continue

        if artifact_path.is_dir():
            shutil.rmtree(artifact_path)
        else:
            artifact_path.unlink(missing_ok=True)

    for egg_info in package_root.glob("*.egg-info"):
        if egg_info.is_dir():
            shutil.rmtree(egg_info, ignore_errors=True)
        else:
            egg_info.unlink(missing_ok=True)


def build_python_package(package_root: Path, *, clean: bool = True) -> bool:
    log_and_print("🔨 Building package...")

    if clean:
        clean_python_build_artifacts(package_root)

    result = subprocess.run(
        [sys.executable, "-m", "build"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(package_root),
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        log_and_print(
            f"❌ Build failed: {stderr or 'unknown build error'}",
            level="error",
        )
        return False

    log_and_print("✅ Package built successfully")
    return True
