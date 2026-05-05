import subprocess

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.release_pipelines.utils import build_context


def check_git_status(**kwargs) -> None:
    log_and_print("🔍 Checking Git status...")

    result = subprocess.run(["git", "status", "--porcelain"],
                            capture_output=True, text=True)

    if result.returncode != 0:
        log_and_print("❌ Not a Git repository", level="error")
        return

    if result.stdout.strip():
        log_and_print("⚠️ Uncommitted changes found:")
        log_and_print(result.stdout)
        return

    log_and_print("✅ Git repository is clean")


def create_git_tag(**kwargs) -> None:
    ctx = build_context(**kwargs)
    version = ctx.version

    log_and_print(f"🏷️ Creating Git tag: v{version}")

    if ctx.dry_run:
        log_and_print("🔍 DRY RUN: Would create tag")
        return

    result = subprocess.run(["git", "tag", f"v{version}"],
                            capture_output=True, text=True)

    if result.returncode != 0:
        log_and_print(f"❌ Tag creation failed: {result.stderr}", level="error")
        return

    log_and_print(f"✅ Git tag v{version} created")


def push_to_remote(**kwargs) -> None:
    ctx = build_context(**kwargs)

    log_and_print("📤 Pushing to remote...")

    if ctx.dry_run:
        log_and_print("🔍 DRY RUN: Would push to remote")
        return

    result = subprocess.run(["git", "push"], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        log_and_print(f"❌ Push failed: {result.stderr}", level="error")
        return

    result = subprocess.run(["git", "push", "--tags"], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        log_and_print(f"❌ Tag push failed: {result.stderr}", level="error")
        return

    log_and_print("✅ Pushed to remote successfully")