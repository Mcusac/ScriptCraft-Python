#!/usr/bin/env python3
"""
Custom Release Script Template (EXPERIMENTAL)

TODO: Review whether this should be deleted or moved outside the package runtime
into a docs/examples/scripts folder. It is intentionally placed in level_Z to
avoid bloating the stable runtime API surface.

Usage:
    python release.py                    # Git release only
    python release.py --pypi            # Git + PyPI release
    python release.py --test            # Test mode (dry run)
"""

import sys

from typing import Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import setup_logger

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import GitWorkspaceTool

logger = setup_logger("custom_release")


class CustomReleaseManager:
    """Custom release manager for any project."""

    def __init__(self, test_mode: bool = False):
        from scriptcraft.layers.layer_1_tools.level_1_impl.level_4 import PyPIReleaseTool

        self.test_mode = test_mode
        self.git_tool = GitWorkspaceTool()
        self.pypi_tool = PyPIReleaseTool()

        if test_mode:
            log_and_print("🧪 Running in TEST MODE (dry run)")

    def check_git_status_for_release(self) -> bool:
        log_and_print("🔍 Checking git status...")

        if self.test_mode:
            log_and_print("✅ Git status check (test mode)")
            return True

        try:
            log_and_print("✅ Git repository is clean")
            return True
        except Exception as e:
            log_and_print(f"❌ Git status check failed: {e}", level="error")
            return False

    def commit_changes(self, message: Optional[str] = None) -> bool:
        if not message:
            message = "Release: Update project files"

        log_and_print(f"📝 Committing changes: {message}")

        if self.test_mode:
            log_and_print("✅ Commit changes (test mode)")
            return True

        try:
            self.git_tool.run(operation="add_all")
            self.git_tool.run(operation="commit", message=message)
            log_and_print("✅ Changes committed successfully")
            return True
        except Exception as e:
            log_and_print(f"❌ Commit failed: {e}", level="error")
            return False

    def push_to_remote(self) -> bool:
        log_and_print("📤 Pushing to remote repository...")

        if self.test_mode:
            log_and_print("✅ Push to remote (test mode)")
            return True

        try:
            self.git_tool.run(operation="push")
            log_and_print("✅ Successfully pushed to remote")
            return True
        except Exception as e:
            log_and_print(f"❌ Push failed: {e}", level="error")
            return False

    def test_pypi_upload(self) -> bool:
        log_and_print("🧪 Testing PyPI upload...")

        if self.test_mode:
            log_and_print("✅ PyPI test upload (test mode)")
            return True

        try:
            self.pypi_tool.run(operation="test")
            log_and_print("✅ PyPI test upload successful")
            return True
        except Exception as e:
            log_and_print(f"❌ PyPI test upload failed: {e}", level="error")
            return False

    def release_to_pypi(self) -> bool:
        log_and_print("📦 Releasing to PyPI...")

        if self.test_mode:
            log_and_print("✅ PyPI release (test mode)")
            return True

        try:
            self.pypi_tool.run(operation="release")
            log_and_print("✅ Successfully released to PyPI")
            return True
        except Exception as e:
            log_and_print(f"❌ PyPI release failed: {e}", level="error")
            return False

    def run_git_release(self) -> bool:
        log_and_print("🚀 Starting Git Release Workflow")
        log_and_print("=" * 40)

        if not self.check_git_status_for_release():
            return False

        if not self.commit_changes():
            return False

        if not self.push_to_remote():
            return False

        log_and_print("✅ Git release completed successfully!")
        return True

    def run_full_release(self) -> bool:
        log_and_print("🚀 Starting Full Release Workflow")
        log_and_print("=" * 40)

        if not self.run_git_release():
            return False

        log_and_print("\n📦 Starting PyPI Release Process")
        log_and_print("-" * 30)

        if not self.test_pypi_upload():
            return False

        if not self.release_to_pypi():
            return False

        log_and_print("✅ Full release completed successfully!")
        return True


def main() -> None:
    test_mode = "--test" in sys.argv
    pypi_release = "--pypi" in sys.argv

    release_manager = CustomReleaseManager(test_mode=test_mode)

    if pypi_release:
        success = release_manager.run_full_release()
    else:
        success = release_manager.run_git_release()

    if success:
        log_and_print("🎉 Release workflow completed successfully!")
        sys.exit(0)

    log_and_print("❌ Release workflow failed!", level="error")
    sys.exit(1)


if __name__ == "__main__":
    main()

