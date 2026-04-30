"""
Python package release steps.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

from pathlib import Path
from typing import Any

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print


def validate_package(*, package_root: Path, **_: Any) -> None:
    """Validate package integrity."""
    log_and_print("🔍 Validating package...")

    required_files = ["pyproject.toml", "README.md"]
    for file in required_files:
        if not (package_root / file).exists():
            log_and_print(f"❌ Missing required file: {file}", level="error")
            return

    tests_dir = package_root / "tests"
    if tests_dir.exists():
        test_file = tests_dir / "test_package_integrity.py"
        if test_file.exists():
            log_and_print("🧪 Running validation tests...")
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env,
                cwd=str(package_root),
            )
            if result.returncode != 0:
                log_and_print(f"❌ Validation tests failed: {result.stderr}", level="error")
                return

    log_and_print("✅ Package validation passed")


def run_tests(*, package_root: Path, **_: Any) -> None:
    """Run package tests."""
    log_and_print("🧪 Running tests...")

    tests_dir = package_root / "tests"
    if not tests_dir.exists():
        log_and_print("⚠️ No tests directory found, skipping tests", level="warning")
        return

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v"],
            capture_output=True,
            text=True,
            cwd=str(package_root),
        )
        if result.returncode != 0:
            log_and_print(f"❌ Tests failed: {result.stderr}", level="error")
            return
    except FileNotFoundError:
        test_files = list(tests_dir.glob("test_*.py"))
        for test_file in test_files:
            log_and_print(f"Running {test_file}...")
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                cwd=str(package_root),
            )
            if result.returncode != 0:
                log_and_print(f"❌ {test_file} failed: {result.stderr}", level="error")
                return

    log_and_print("✅ All tests passed")


def build_package(*, package_root: Path, **_: Any) -> None:
    """Build the package."""
    log_and_print("🔨 Building package...")

    for artifact in ["build", "dist", "*.egg-info"]:
        artifact_path = package_root / artifact
        if artifact_path.exists():
            if artifact_path.is_dir():
                shutil.rmtree(artifact_path)
            else:
                artifact_path.unlink()

    result = subprocess.run(
        [sys.executable, "-m", "build"],
        capture_output=True,
        text=True,
        cwd=str(package_root),
    )
    if result.returncode != 0:
        log_and_print(f"❌ Build failed: {result.stderr}", level="error")
        return

    log_and_print("✅ Package built successfully")


def upload_to_pypi(*, package_root: Path, dry_run: bool, **_: Any) -> None:
    """Upload package to PyPI."""
    log_and_print("📦 Uploading to PyPI...")

    if dry_run:
        log_and_print("🔍 DRY RUN: Would upload to PyPI")
        return

    result = subprocess.run(
        [sys.executable, "-m", "twine", "upload", "dist/*"],
        capture_output=True,
        text=True,
        cwd=str(package_root),
    )
    if result.returncode != 0:
        log_and_print(f"❌ Upload failed: {result.stderr}", level="error")
        return

    log_and_print("✅ Package uploaded to PyPI")

