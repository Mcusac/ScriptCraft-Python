#!/usr/bin/env python3
"""
🚀 Pre-Upload Validation Script

Run this script before uploading to PyPI to ensure everything is working correctly.
"""

import sys
import subprocess

from pathlib import Path
from typing import Tuple

def run_command(cmd: str, description: str) -> Tuple[bool, str]:
    """Run a command and return success status and output."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True, result.stdout
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ {description} - EXCEPTION: {e}")
        return False, str(e)

def validate_package():
    """Validate the package before upload."""
    print("🚀 Pre-Upload Validation")
    print("=" * 50)
    
    # Change to package directory
    package_dir = Path(__file__).parent
    original_dir = Path.cwd()
    
    try:
        # 1. Test imports
        print("\n📦 Testing Package Imports...")
        success, output = run_command(
            "python tests/test_import_patterns.py",
            "Import pattern tests"
        )
        if not success:
            return False
        
        # 2. Test package integrity
        print("\n🧪 Testing Package Integrity...")
        success, output = run_command(
            "python tests/test_package_integrity.py", 
            "Package integrity tests"
        )
        if not success:
            return False
        
        # 3. Check package build
        print("\n🔨 Testing Package Build...")
        success, output = run_command(
            "python -m build --wheel",
            "Package wheel build"
        )
        if not success:
            return False
        
        # 4. Check package metadata
        print("\n📋 Checking Package Metadata...")
        success, output = run_command(
            "python -c \"import scriptcraft; print(f'Version: {scriptcraft.__version__}')\"",
            "Package metadata check"
        )
        if not success:
            return False
        
        # 5. Test console scripts
        print("\n🖥️ Testing Console Scripts...")
        scripts_to_test = [
            "scriptcraft --help",
            "rhq-autofiller --help", 
            "data-comparer --help",
            "auto-labeler --help",
            "function-auditor --help"
        ]
        
        for script in scripts_to_test:
            success, output = run_command(script, f"Console script: {script.split()[0]}")
            if not success:
                print(f"⚠️ Warning: {script} failed (may be expected if not installed)")
        
        # 6. Check for common issues
        print("\n🔍 Checking for Common Issues...")
        
        # Check for hardcoded paths
        pyproject_path = package_dir / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text()
            if "localhost" in content or "127.0.0.1" in content:
                print("⚠️ Warning: Found localhost/127.0.0.1 in pyproject.toml")
        
        # Check version consistency
        try:
            import scriptcraft
            from scriptcraft._version import __version__
            if scriptcraft.__version__ != __version__:
                print(f"❌ Version mismatch: {scriptcraft.__version__} vs {__version__}")
                return False
            else:
                print(f"✅ Version consistent: {__version__}")
        except Exception as e:
            print(f"❌ Version check failed: {e}")
            return False
        
        print("\n" + "=" * 50)
        print("✅ All validation checks passed!")
        print("🚀 Package is ready for upload!")
        return True
        
    except Exception as e:
        print(f"❌ Validation failed with exception: {e}")
        return False
    finally:
        # Clean up build artifacts
        print("\n🧹 Cleaning up build artifacts...")
        import shutil
        for artifact in ["build", "dist", "*.egg-info"]:
            artifact_path = package_dir / artifact
            if artifact_path.exists():
                if artifact_path.is_dir():
                    shutil.rmtree(artifact_path)
                else:
                    artifact_path.unlink()

def main():
    """Main validation function."""
    success = validate_package()
    
    if success:
        print("\n🎉 Validation successful! You can now upload to PyPI.")
        print("\nNext steps:")
        print("1. python -m build")
        print("2. python -m twine upload dist/*")
    else:
        print("\n❌ Validation failed! Please fix the issues before uploading.")
        sys.exit(1)

if __name__ == "__main__":
    main()
