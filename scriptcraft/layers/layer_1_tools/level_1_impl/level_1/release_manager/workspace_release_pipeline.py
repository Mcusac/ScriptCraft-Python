"""Workspace release DAG orchestration."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from scriptcraft.layers.layer_0_core.level_1 import run_command

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import get_commit_message, log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import bump_version
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    ensure_tag,
    git_status_porcelain,
    push_main_and_tag,
    stage_all,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    get_current_workspace_version,
    get_phase_name,
    update_changelog,
    update_version_file,
)


@dataclass
class WorkspaceReleaseContext:
    input_paths: List[Path]
    output_dir: Path
    domain: Optional[str]
    version_type: str
    auto_push: bool
    force: bool
    custom_message: Optional[str]

    current_version: Optional[str] = None
    new_version: Optional[str] = None
    status: Optional[str] = None
    tag_exists: bool = False


class WorkspaceReleasePipeline:
    def __init__(self, ctx: WorkspaceReleaseContext) -> None:
        self.ctx = ctx

    def run(self) -> None:
        log_and_print("🚀 Running Workspace Release Mode...")
        if not self._validate():
            return
        if not self._resolve_versions():
            return
        self._print_header()
        if not self._run_version_step():
            return
        if not self._run_changelog_step():
            return
        if not self._run_git_stage():
            return
        if not self._run_status_check():
            return
        if not self._run_commit():
            return
        if not self._run_tag():
            return
        if not self._run_push():
            return
        self._run_report()

    def _validate(self) -> bool:
        if not self.ctx.version_type:
            log_and_print("❌ Version type required", level="error")
            return False
        if self.ctx.version_type not in ["major", "minor", "patch"]:
            log_and_print("❌ Invalid version type", level="error")
            return False
        return True

    def _resolve_versions(self) -> bool:
        self.ctx.current_version = get_current_workspace_version()
        if not self.ctx.current_version:
            return False
        self.ctx.new_version = bump_version(self.ctx.current_version, self.ctx.version_type)
        return bool(self.ctx.new_version)

    def _run_version_step(self) -> bool:
        return update_version_file(self.ctx.new_version)

    def _run_changelog_step(self) -> bool:
        return update_changelog(self.ctx.new_version, self.ctx.version_type)

    def _run_git_stage(self) -> bool:
        return stage_all(Path.cwd(), "Staging all changes")

    def _run_status_check(self) -> bool:
        self.ctx.status = git_status_porcelain(Path.cwd(), "Checking git status")
        if self.ctx.status is None:
            return False
        if not self.ctx.status and not self.ctx.force:
            log_and_print("⚠️ No changes to commit", level="warning")
            return False
        return True

    def _run_commit(self) -> bool:
        msg = (
            self.ctx.custom_message
            or get_commit_message(
                self.ctx.new_version,
                self.ctx.version_type,
                subject="Workspace",
            )
        )
        log_and_print("🔍 Creating commit...")
        result = run_command(["git", "commit", "-m", str(msg)], check=False, cwd=Path.cwd())
        if int(result["returncode"]) == 0:
            log_and_print("✅ Creating commit - SUCCESS")
            return True
        log_and_print("❌ Creating commit - FAILED", level="error")
        stderr = (result.get("stderr") or "").strip()
        if stderr:
            log_and_print(f"Error: {stderr}", level="error")
        return False

    def _run_tag(self) -> bool:
        result = run_command(
            ["git", "tag", "-l", f"v{self.ctx.new_version}"],
            check=False,
            cwd=Path.cwd(),
        )
        tag_check = (result.get("stdout") or "").strip()
        self.ctx.tag_exists = bool(tag_check)
        if self.ctx.tag_exists:
            log_and_print(f"⚠️ Tag v{self.ctx.new_version} exists")
            return True
        return ensure_tag(Path.cwd(), self.ctx.new_version)

    def _run_push(self) -> bool:
        if not self.ctx.auto_push:
            return True
        log_and_print("🚀 Pushing to remote...")
        return push_main_and_tag(Path.cwd(), self.ctx.new_version)

    def _print_header(self) -> None:
        log_and_print("🎯 Workspace Release Process")
        log_and_print(f"🔄 {self.ctx.current_version} → {self.ctx.new_version}")
        log_and_print(f"📋 Phase: {get_phase_name(self.ctx.new_version)}")
        log_and_print("=" * 50)

    def _run_report(self) -> None:
        log_and_print("=" * 50)
        log_and_print(f"🎉 Workspace v{self.ctx.new_version} released!")
        log_and_print(f"📋 Phase: {get_phase_name(self.ctx.new_version)}")
        log_and_print("\n✅ Completed:")
        log_and_print(f"   • VERSION updated → {self.ctx.new_version}")
        log_and_print("   • CHANGELOG updated")
        log_and_print("   • Commit created")
        log_and_print("   • Tag created")
        if self.ctx.auto_push:
            log_and_print("   • Pushed to remote")
        log_and_print("\n📝 Next steps:")
        log_and_print("   • Review CHANGELOG")
        log_and_print("   • Push if not auto-pushed")
        log_and_print("   • Publish release notes")
        tag_r = run_command(
            ["git", "describe", "--tags", "--abbrev=0"],
            check=False,
            cwd=Path.cwd(),
        )
        tag = (tag_r.get("stdout") or "").strip()
        if tag:
            log_and_print(f"Latest tag: {tag}")
