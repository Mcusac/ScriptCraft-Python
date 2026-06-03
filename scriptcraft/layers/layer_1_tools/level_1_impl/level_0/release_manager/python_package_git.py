"""Python-package and workspace git steps (shared L0 mechanics)."""

import os

from pathlib import Path
from typing import Optional

from scriptcraft.layers.layer_0_core.level_1 import run_command

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import get_commit_message, log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    commit_if_needed,
    ensure_tag,
    git_status_porcelain,
    push_main_and_tag,
    stage_path,
    submodule_update_remote,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_5 import load_config


def get_workspace_version_strategy() -> str:
    env_value = os.environ.get("WORKSPACE_VERSION_STRATEGY")
    if env_value:
        return env_value.strip().lower()
    try:
        config = load_config()
        if config is not None:
            framework_cfg = (
                config.get_framework_config()
                if hasattr(config, "get_framework_config")
                else None
            )
            packaging = getattr(framework_cfg, "packaging", None)
            if isinstance(packaging, dict):
                value = packaging.get("workspace_version_strategy")
                if isinstance(value, str) and value.strip():
                    return value.strip().lower()
    except Exception:
        pass
    return "mirror"


def finalize_submodule_git(
    submodule_dir: Path,
    *,
    new_version: str,
    version_type: str,
    auto_push: bool,
    force: bool,
    custom_message: Optional[str],
) -> bool:
    if git_status_porcelain(submodule_dir, "Checking git status") is None:
        return False
    commit_message = custom_message or get_commit_message(new_version, version_type)
    if not commit_if_needed(
        submodule_dir,
        commit_message,
        force=force,
        status_label="Checking staged changes",
    ):
        return False
    ensure_tag(submodule_dir, new_version)
    if auto_push:
        push_main_and_tag(submodule_dir, new_version)
    return True


def sync_workspace_submodule_ref(
    workspace_root: Path,
    *,
    new_version: str,
    auto_push: bool,
) -> bool:
    log_and_print("🔄 Updating workspace reference...")
    submodule_update_remote(workspace_root)
    if not stage_path(workspace_root, "implementations/python-package", "Staging submodule ref"):
        return True
    result = run_command(
        ["git", "commit", "-m", f"📦 Update python-package v{new_version}"],
        check=False,
        cwd=workspace_root,
    )
    if int(result["returncode"]) != 0:
        log_and_print("❌ Committing workspace update - FAILED", level="error")
        stderr = (result.get("stderr") or "").strip()
        if stderr:
            log_and_print(f"Error: {stderr}", level="error")
        return False
    log_and_print("✅ Committing workspace update - SUCCESS")
    if auto_push:
        push_r = run_command(["git", "push", "origin", "main"], check=False, cwd=workspace_root)
        if int(push_r["returncode"]) != 0:
            log_and_print("❌ Pushing workspace - FAILED", level="error")
            return False
        log_and_print("✅ Pushing workspace - SUCCESS")
    return True


def mirror_workspace_version_file(
    workspace_root: Path,
    *,
    new_version: str,
    auto_push: bool,
) -> None:
    if get_workspace_version_strategy() != "mirror":
        return
    try:
        version_file = workspace_root / "VERSION"
        version_file.write_text(f"{new_version}\n", encoding="utf-8")
        add_r = run_command(["git", "add", "VERSION"], check=False, cwd=workspace_root)
        if int(add_r["returncode"]) == 0:
            commit_r = run_command(
                ["git", "commit", "-m", f"Workspace v{new_version} (mirror)"],
                check=False,
                cwd=workspace_root,
            )
            if int(commit_r["returncode"]) != 0:
                log_and_print("❌ Committing workspace version - FAILED", level="error")
            tag_r = run_command(
                ["git", "tag", "-l", f"v{new_version}"],
                check=False,
                cwd=workspace_root,
            )
            if not (tag_r.get("stdout") or "").strip():
                ensure_tag(workspace_root, new_version)
            if auto_push:
                push_main_and_tag(workspace_root, new_version)
    except Exception as exc:
        log_and_print(f"⚠️ Mirror failed: {exc}", level="warning")
