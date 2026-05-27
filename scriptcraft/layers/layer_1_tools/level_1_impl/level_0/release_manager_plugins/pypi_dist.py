"""Shared PyPI distribution directory helpers for release plugins."""

from pathlib import Path
from typing import List, Optional

from scriptcraft.layers.layer_0_core.level_1 import run_command

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print


def list_distribution_files(dist_dir: Path) -> List[Path]:
    return list(dist_dir.glob("*.whl")) + list(dist_dir.glob("*.tar.gz"))


def check_dist_directory(dist_dir: Optional[Path] = None) -> bool:
    """Check that a dist directory exists and contains package files."""
    resolved = dist_dir or Path("dist")

    if not resolved.exists():
        log_and_print("❌ dist/ directory not found", level="error")
        log_and_print("💡 Build the package first: python -m build", level="error")
        return False

    package_files = list_distribution_files(resolved)

    if not package_files:
        log_and_print("❌ No package files found in dist/", level="error")
        log_and_print("💡 Build the package first: python -m build", level="error")
        return False

    log_and_print(f"📦 Found {len(package_files)} package file(s):")
    for file in package_files:
        size_kb = file.stat().st_size / 1024
        log_and_print(f"   • {file.name} ({size_kb:.1f} KB)")

    return True


def validate_distribution_files(
    dist_dir: Path,
    *,
    cwd: Optional[Path] = None,
) -> bool:
    """Validate package files using twine check."""
    package_files = list_distribution_files(dist_dir)
    if not package_files:
        log_and_print("❌ No package files found in dist/", level="error")
        return False

    log_and_print("🔍 Validating package files...")
    result = run_command(
        ["python", "-m", "twine", "check", *[str(path) for path in package_files]],
        check=False,
        cwd=cwd,
    )
    if int(result["returncode"]) == 0:
        log_and_print("✅ Validating package files - SUCCESS")
        return True

    log_and_print("❌ Validating package files - FAILED", level="error")
    stderr = (result.get("stderr") or "").strip()
    if stderr:
        log_and_print(f"Error: {stderr}", level="error")
    return False


def upload_distribution_files(
    dist_dir: Path,
    *,
    cwd: Optional[Path] = None,
) -> bool:
    """Upload wheel/sdist files from a dist directory to PyPI."""
    package_files = list_distribution_files(dist_dir)
    if not package_files:
        log_and_print("❌ No package files found in dist/", level="error")
        return False

    log_and_print("🔍 Uploading to PyPI...")
    result = run_command(
        ["python", "-m", "twine", "upload", *[str(path) for path in package_files]],
        check=False,
        cwd=cwd,
    )
    if int(result["returncode"]) == 0:
        log_and_print("✅ Uploading to PyPI - SUCCESS")
        return True

    log_and_print("❌ Uploading to PyPI - FAILED", level="error")
    stderr = (result.get("stderr") or "").strip()
    if stderr:
        log_and_print(f"Error: {stderr}", level="error")
    return False
