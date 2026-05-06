"""
PyPI Upload Plugin for Release Manager Tool.

This plugin handles uploading existing packages to PyPI without version changes.
Useful for re-uploading packages or uploading packages built elsewhere.
"""

from pathlib import Path
from typing import List, Optional

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.subprocess.runner import run_ok


# ============================================================
# VALIDATION
# ============================================================

def check_dist_directory() -> bool:
    """Check if dist directory exists and contains package files."""
    dist_dir = Path("dist")

    if not dist_dir.exists():
        log_and_print("❌ dist/ directory not found", level="error")
        log_and_print("💡 Build the package first: python -m build", level="error")
        return False

    package_files = list(dist_dir.glob("*.whl")) + list(dist_dir.glob("*.tar.gz"))

    if not package_files:
        log_and_print("❌ No package files found in dist/", level="error")
        log_and_print("💡 Build the package first: python -m build", level="error")
        return False

    log_and_print(f"📦 Found {len(package_files)} package file(s):")

    for file in package_files:
        size_kb = file.stat().st_size / 1024
        log_and_print(f"   • {file.name} ({size_kb:.1f} KB)")

    return True


def validate_package_files() -> bool:
    """Validate package files using twine check."""
    return run_ok("python -m twine check dist/*", "Validating package files")


def upload_to_pypi() -> bool:
    """Upload package to PyPI."""
    return run_ok("python -m twine upload dist/*", "Uploading to PyPI")


# ============================================================
# MAIN ENTRYPOINT
# ============================================================

def run_mode(
    input_paths: List[Path],
    output_dir: Path,
    domain: Optional[str] = None,
    **kwargs,
) -> None:
    """
    Run PyPI upload mode.
    """

    log_and_print("📦 Running PyPI Upload Mode...")
    log_and_print("=" * 50)

    # --------------------------------------------------------
    # STEP 1: CHECK DIST
    # --------------------------------------------------------
    if not check_dist_directory():
        return

    # --------------------------------------------------------
    # STEP 2: VALIDATE PACKAGE
    # --------------------------------------------------------
    if not validate_package_files():
        log_and_print("❌ Package validation failed. Aborting upload.", level="error")
        return

    # --------------------------------------------------------
    # STEP 3: UPLOAD
    # --------------------------------------------------------
    if not upload_to_pypi():
        log_and_print("❌ PyPI upload failed.", level="error")
        return

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------
    log_and_print("=" * 50)
    log_and_print("🎉 Successfully uploaded package to PyPI!")

    log_and_print("\n✅ Completed:")
    log_and_print("   • Package validation passed")
    log_and_print("   • Upload to PyPI successful")

    # --------------------------------------------------------
    # NEXT STEPS
    # --------------------------------------------------------
    log_and_print("\n📝 Next steps:")
    log_and_print("   1. Verify package on PyPI")
    log_and_print("   2. Test installation:")
    log_and_print("      pip install <package-name>")
    log_and_print("   3. Update dependent services if needed")

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------
    dist_dir = Path("dist")

    if dist_dir.exists():
        package_files = list(dist_dir.glob("*.whl")) + list(dist_dir.glob("*.tar.gz"))

        log_and_print("\n📊 Current status:")
        log_and_print(f"Package files: {len(package_files)}")

        for file in package_files:
            size_kb = file.stat().st_size / 1024
            log_and_print(f"   • {file.name} ({size_kb:.1f} KB)")