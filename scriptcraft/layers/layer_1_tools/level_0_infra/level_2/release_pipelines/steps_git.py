"""
Git release pipeline steps — canonical implementation via GitService.

Supports kwargs from StepPipelineEngine global steps and explicit repo_root/version/dry_run
from generic release tooling.
"""

from pathlib import Path
from typing import Any

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import GitService
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import ReleasePipelineContext


def _resolve_repo_root(kwargs: dict[str, Any]) -> Path:
    root = kwargs.get("repo_root")
    if root is not None:
        return Path(root)

    config = kwargs.get("config")
    workspace_root = getattr(config, "workspace_root", None) if config is not None else None
    if workspace_root is not None:
        return Path(workspace_root)

    return Path.cwd()


def _git(kwargs: dict[str, Any]) -> GitService:
    return GitService(repo_root=_resolve_repo_root(kwargs))


def check_git_status(**kwargs: Any) -> None:
    log_and_print("🔍 Checking Git status...")

    git = _git(kwargs)

    if not git.is_repo():
        log_and_print("❌ Not a Git repository", level="error")
        return

    if git.has_changes():
        log_and_print("⚠️ Uncommitted changes found:", level="warning")
        log_and_print(git.status_porcelain(), level="warning")
        return

    log_and_print("✅ Git repository is clean")


def create_git_tag(**kwargs: Any) -> None:
    ctx = ReleasePipelineContext(
        version=kwargs.get("version", "0.0.0"),
        dry_run=kwargs.get("dry_run", False),
        repo_root=kwargs.get("repo_root"),
        package_root=kwargs.get("package_root"),
        docs_root=kwargs.get("docs_root"),
        timestamp=kwargs.get("timestamp"),
        extras=kwargs,
    )
    version = str(ctx.version)

    log_and_print(f"🏷️ Creating Git tag: v{version}")

    if ctx.dry_run:
        log_and_print("🔍 DRY RUN: Would create tag")
        return

    git = _git(kwargs)

    if not git.create_tag(version):
        log_and_print("❌ Tag creation failed", level="error")
        return

    log_and_print(f"✅ Git tag v{version} created")


def push_to_remote(**kwargs: Any) -> None:
    ctx = ReleasePipelineContext(
        version=kwargs.get("version", "0.0.0"),
        dry_run=kwargs.get("dry_run", False),
        repo_root=kwargs.get("repo_root"),
        package_root=kwargs.get("package_root"),
        docs_root=kwargs.get("docs_root"),
        timestamp=kwargs.get("timestamp"),
        extras=kwargs,
    )

    log_and_print("📤 Pushing to remote...")

    if ctx.dry_run:
        log_and_print("🔍 DRY RUN: Would push to remote")
        return

    git = _git(kwargs)

    if not git.push():
        log_and_print("❌ Push failed", level="error")
        return

    if not git.push_tags():
        log_and_print("❌ Tag push failed", level="error")
        return

    log_and_print("✅ Pushed to remote successfully")
