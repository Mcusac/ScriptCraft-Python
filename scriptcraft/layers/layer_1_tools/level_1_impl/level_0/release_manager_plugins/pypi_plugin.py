"""
PyPI Upload Plugin for Release Manager Tool.

This plugin handles uploading existing packages to PyPI without version changes.
Useful for re-uploading packages or uploading packages built elsewhere.
"""

import subprocess

from pathlib import Path
from typing import List, Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print


def run_command(command: str, description: str, cwd: Optional[Path] = None) -> Optional[str]:
    """Run a command and handle errors."""
    log_and_print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, 
            check=True, encoding='utf-8', errors='replace', cwd=cwd
        )
        log_and_print(f"✅ {description} completed")
        return result.stdout.strip() if result.stdout else ""
    except subprocess.CalledProcessError as e:
        log_and_print(f"❌ {description} failed: {e}", level="error")
        if e.stderr:
            # Handle potential encoding issues in stderr
            try:
                error_output = e.stderr
            except UnicodeDecodeError:
                error_output = e.stderr.encode('utf-8', errors='replace').decode('utf-8')
            log_and_print(f"Error output: {error_output}", level="error")
        return None
    except UnicodeDecodeError as e:
        log_and_print(f"❌ {description} failed due to encoding issue: {e}", level="error")
        return None


def check_dist_directory() -> bool:
    """Check if dist directory exists and contains package files."""
    dist_dir = Path("dist")
    if not dist_dir.exists():
        log_and_print("❌ dist/ directory not found", level="error")
        log_and_print("💡 Build the package first with: python -m build", level="error")
        return False
    
    package_files = list(dist_dir.glob("*.whl")) + list(dist_dir.glob("*.tar.gz"))
    if not package_files:
        log_and_print("❌ No package files found in dist/ directory", level="error")
        log_and_print("💡 Build the package first with: python -m build", level="error")
        return False
    
    log_and_print(f"📦 Found {len(package_files)} package files in dist/")
    for file in package_files:
        log_and_print(f"   • {file.name}")
    
    return True


def validate_package_files() -> bool:
    """Validate package files using twine check."""
    return run_command("python -m twine check dist/*", "Validating package files") is not None


def upload_to_pypi() -> bool:
    """Upload package to PyPI."""
    return run_command("python -m twine upload dist/*", "Uploading to PyPI") is not None


def run_mode(input_paths: List[Path], output_dir: Path, domain: Optional[str] = None, 
             **kwargs) -> None:
    """
    Run PyPI upload mode.
    
    Args:
        input_paths: List of input paths (not used for this plugin)
        output_dir: Output directory (not used for this plugin)
        domain: Domain context (not used for this plugin)
        **kwargs: Additional arguments
    """
    log_and_print("📦 Running PyPI Upload Mode...")
    log_and_print("=" * 50)
    
    # Step 1: Check if dist directory exists
    if not check_dist_directory():
        return
    
    # Step 2: Validate package files
    if not validate_package_files():
        log_and_print("❌ Package validation failed. Aborting upload.", level="error")
        return
    
    # Step 3: Upload to PyPI
    if not upload_to_pypi():
        log_and_print("❌ PyPI upload failed.", level="error")
        return
    
    # Success!
    log_and_print("=" * 50)
    log_and_print("🎉 Successfully uploaded package to PyPI!")
    
    # Show what was done
    log_and_print("\n✅ Completed:")
    log_and_print("   • Validated package files")
    log_and_print("   • Uploaded to PyPI")
    
    # Show next steps
    log_and_print("\n📝 Next steps:")
    log_and_print("   1. Verify the package on PyPI")
    log_and_print("   2. Test installation: pip install <package-name>")
    log_and_print("   3. Update any dependent projects if needed")
    
    # Show current status
    log_and_print(f"\n📊 Current status:")
    dist_dir = Path("dist")
    if dist_dir.exists():
        package_files = list(dist_dir.glob("*.whl")) + list(dist_dir.glob("*.tar.gz"))
        log_and_print(f"Package files in dist/: {len(package_files)}")
        for file in package_files:
            log_and_print(f"   • {file.name} ({file.stat().st_size / 1024:.1f} KB)")
