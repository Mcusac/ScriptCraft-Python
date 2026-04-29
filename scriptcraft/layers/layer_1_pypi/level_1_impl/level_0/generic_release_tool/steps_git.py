"""
Git repository release steps.
"""

from __future__ import annotations

import subprocess

from pathlib import Path
from typing import Any

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print


def check_git_status(*, repo_root: Path, **_: Any) -> None:
    """Check Git repository status."""
    log_and_print("🔍 Checking Git status...")

    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=str(repo_root),
    )
    if result.returncode != 0:
        log_and_print("❌ Not a Git repository", level="error")
        return

    if result.stdout.strip():
        log_and_print("⚠️ Uncommitted changes found:", level="warning")
        log_and_print(result.stdout)
        return

    log_and_print("✅ Git repository is clean")


def create_git_tag(*, repo_root: Path, version: str, dry_run: bool, **_: Any) -> None:
    """Create a Git tag."""
    log_and_print(f"🏷️ Creating Git tag: v{version}")

    if dry_run:
        log_and_print("🔍 DRY RUN: Would create tag")
        return

    result = subprocess.run(
        ["git", "tag", f"v{version}"],
        capture_output=True,
        text=True,
        cwd=str(repo_root),
    )
    if result.returncode != 0:
        log_and_print(f"❌ Tag creation failed: {result.stderr}", level="error")
        return

    log_and_print(f"✅ Git tag v{version} created")


def push_to_remote(*, repo_root: Path, dry_run: bool, **_: Any) -> None:
    """Push to remote repository."""
    log_and_print("📤 Pushing to remote...")

    if dry_run:
        log_and_print("🔍 DRY RUN: Would push to remote")
        return

    result = subprocess.run(["git", "push"], capture_output=True, text=True, encoding="utf-8", cwd=str(repo_root))
    if result.returncode != 0:
        log_and_print(f"❌ Push failed: {result.stderr}", level="error")
        return

    result = subprocess.run(
        ["git", "push", "--tags"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(repo_root),
    )
    if result.returncode != 0:
        log_and_print(f"❌ Tag push failed: {result.stderr}", level="error")
        return

    log_and_print("✅ Pushed to remote successfully")

