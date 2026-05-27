"""
PyPI upload plugin for Release Manager.

Uploads existing packages from dist/ without version changes.
"""

from pathlib import Path
from typing import List, Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    check_dist_directory,
    upload_distribution_files,
    validate_distribution_files,
    list_distribution_files,
)

def check_dist_directory_at_cwd() -> bool:
    return check_dist_directory(Path("dist"))


def validate_package_files() -> bool:
    return validate_distribution_files(Path("dist"))


def upload_to_pypi() -> bool:
    return upload_distribution_files(Path("dist"))


def pypi_upload_mode(
    input_paths: List[Path],
    output_dir: Path,
    domain: Optional[str] = None,
    **kwargs,
) -> None:
    """Run PyPI upload mode (validate dist/ then upload)."""
    _ = input_paths, output_dir, domain, kwargs

    log_and_print("📦 Running PyPI Upload Mode...")
    log_and_print("=" * 50)

    if not check_dist_directory_at_cwd():
        return

    if not validate_package_files():
        log_and_print("❌ Package validation failed. Aborting upload.", level="error")
        return

    if not upload_to_pypi():
        log_and_print("❌ PyPI upload failed.", level="error")
        return

    log_and_print("=" * 50)
    log_and_print("🎉 Successfully uploaded package to PyPI!")
    log_and_print("\n✅ Completed:")
    log_and_print("   • Package validation passed")
    log_and_print("   • Upload to PyPI successful")
    log_and_print("\n📝 Next steps:")
    log_and_print("   1. Verify package on PyPI")
    log_and_print("   2. Test installation: pip install <package-name>")

    dist_dir = Path("dist")
    if dist_dir.exists():
        package_files = list_distribution_files(dist_dir)
        log_and_print("\n📊 Current status:")
        log_and_print(f"Package files: {len(package_files)}")
        for file in package_files:
            size_kb = file.stat().st_size / 1024
            log_and_print(f"   • {file.name} ({size_kb:.1f} KB)")
