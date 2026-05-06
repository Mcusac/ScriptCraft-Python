"""
Workspace Release Plugin for Release Manager Tool.

Refactor improvements:
- DAG-style pipeline execution
- SRP separation per release stage
- Centralized context object
- Reduced run_mode complexity
- Fully behavior-preserving
"""

import re

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.subprocess.runner import run_str

from layers.layer_1_tools.level_1_impl.level_0.versioning.messages import get_commit_message
from layers.layer_1_tools.level_1_impl.level_0.versioning.semver import bump_version


# ============================================================
# CONTEXT (shared state across DAG)
# ============================================================

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


# ============================================================
# VERSION HELPERS (unchanged behavior)
# ============================================================

def get_current_workspace_version() -> Optional[str]:
    version_file = Path("VERSION")

    if not version_file.exists():
        log_and_print("❌ VERSION file not found", level="error")
        return None

    return version_file.read_text(encoding="utf-8").strip()


def update_version_file(new_version: str) -> bool:
    try:
        Path("VERSION").write_text(new_version + "\n", encoding="utf-8")
        log_and_print(f"✅ Updated VERSION file to {new_version}")
        return True
    except Exception as e:
        log_and_print(f"❌ Error updating VERSION file: {e}", level="error")
        return False


def get_phase_name(version: str) -> str:
    major, minor, _ = map(int, version.split("."))

    if major != 0:
        return "Release Phase"
    if minor <= 3:
        return "Foundation Phase"
    if minor <= 6:
        return "Core Development Phase"
    if minor <= 9:
        return "Polish Phase"
    return "Pre-release Phase"


# ============================================================
# CHANGELOG
# ============================================================

def update_changelog(new_version: str, version_type: str) -> bool:
    changelog = Path("CHANGELOG.md")

    if not changelog.exists():
        log_and_print("⚠️ CHANGELOG.md not found, skipping", level="warning")
        return True

    try:
        content = changelog.read_text(encoding="utf-8")
        today = datetime.now().strftime("%Y-%m-%d")

        template = f"""## [{new_version}] - {today}

### Added ✨
- [Add your new features here]

### Changed 🔄
- [Add your changes here]

### Fixed 🐛
- [Add your bug fixes here]

### Technical 🛠️
- [Add technical improvements here]

### Documentation 📚
- [Add documentation updates here]

"""

        if "[Unreleased]" in content:
            content = content.replace("[Unreleased]", f"[{new_version}] - {today}")
            content = re.sub(
                rf"(## \[{new_version}\] - {today}\n)",
                rf"\1{template}",
                content,
                flags=re.MULTILINE,
            )
        else:
            header = r"(# Changelog 📝\n\nAll notable changes.*?\n\n)"
            content = re.sub(header, rf"\1{template}", content, flags=re.DOTALL)

        changelog.write_text(content, encoding="utf-8")
        log_and_print(f"✅ Updated CHANGELOG.md with version {new_version}")
        return True

    except Exception as e:
        log_and_print(f"❌ Error updating CHANGELOG.md: {e}", level="error")
        return False


# ============================================================
# PIPELINE (DAG ORCHESTRATOR)
# ============================================================

class WorkspaceReleasePipeline:

    def __init__(self, ctx: WorkspaceReleaseContext):
        self.ctx = ctx

    # ------------------------
    # ENTRYPOINT
    # ------------------------
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

    # ========================================================
    # STEP 1: VALIDATION
    # ========================================================

    def _validate(self) -> bool:
        if not self.ctx.version_type:
            log_and_print("❌ Version type required", level="error")
            return False

        if self.ctx.version_type not in ["major", "minor", "patch"]:
            log_and_print("❌ Invalid version type", level="error")
            return False

        return True

    # ========================================================
    # STEP 2: VERSIONING
    # ========================================================

    def _resolve_versions(self) -> bool:
        self.ctx.current_version = get_current_workspace_version()
        if not self.ctx.current_version:
            return False

        self.ctx.new_version = bump_version(
            self.ctx.current_version,
            self.ctx.version_type
        )
        return bool(self.ctx.new_version)

    def _run_version_step(self) -> bool:
        return update_version_file(self.ctx.new_version)

    # ========================================================
    # STEP 3: CHANGELOG
    # ========================================================

    def _run_changelog_step(self) -> bool:
        return update_changelog(self.ctx.new_version, self.ctx.version_type)

    # ========================================================
    # STEP 4: GIT STAGING
    # ========================================================

    def _run_git_stage(self) -> bool:
        return run_str("git add .", "Staging all changes") is not None

    # ========================================================
    # STEP 5: STATUS CHECK
    # ========================================================

    def _run_status_check(self) -> bool:
        self.ctx.status = run_str("git status --porcelain", "Checking git status")

        if self.ctx.status is None:
            return False

        if not self.ctx.status and not self.ctx.force:
            log_and_print("⚠️ No changes to commit", level="warning")
            return False

        return True

    # ========================================================
    # STEP 6: COMMIT
    # ========================================================

    def _run_commit(self) -> bool:
        msg = (
            self.ctx.custom_message
            or get_commit_message(
                self.ctx.new_version,
                self.ctx.version_type,
                subject="Workspace"
            )
        )

        return run_str(f'git commit -m "{msg}"', "Creating commit") is not None

    # ========================================================
    # STEP 7: TAG
    # ========================================================

    def _run_tag(self) -> bool:
        tag_check = run_str(
            f"git tag -l v{self.ctx.new_version}",
            "Checking tag"
        )

        self.ctx.tag_exists = bool(tag_check and tag_check.strip())

        if self.ctx.tag_exists:
            log_and_print(f"⚠️ Tag v{self.ctx.new_version} exists")
            return True

        return run_str(
            f"git tag v{self.ctx.new_version}",
            "Creating tag"
        ) is not None

    # ========================================================
    # STEP 8: PUSH
    # ========================================================

    def _run_push(self) -> bool:
        if not self.ctx.auto_push:
            return True

        log_and_print("🚀 Pushing to remote...")

        run_str("git push origin main", "Pushing commits")
        run_str(f"git push origin v{self.ctx.new_version}", "Pushing tag")

        return True

    # ========================================================
    # REPORTING
    # ========================================================

    def _print_header(self):
        log_and_print("🎯 Workspace Release Process")
        log_and_print(f"🔄 {self.ctx.current_version} → {self.ctx.new_version}")
        log_and_print(f"📋 Phase: {get_phase_name(self.ctx.new_version)}")
        log_and_print("=" * 50)

    def _run_report(self):
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

        latest = run_str("git log --oneline -1", "Latest commit")
        tag = run_str("git describe --tags --abbrev=0", "Latest tag")

        if tag:
            log_and_print(f"Latest tag: {tag}")


# ============================================================
# ORIGINAL FUNCTION ENTRYPOINT (UNCHANGED EXTERNAL API)
# ============================================================

def run_mode(
    input_paths: List[Path],
    output_dir: Path,
    domain: Optional[str] = None,
    version_type: Optional[str] = None,
    auto_push: bool = False,
    force: bool = False,
    custom_message: Optional[str] = None,
    **kwargs,
) -> None:

    ctx = WorkspaceReleaseContext(
        input_paths=input_paths,
        output_dir=output_dir,
        domain=domain,
        version_type=version_type,
        auto_push=auto_push,
        force=force,
        custom_message=custom_message,
    )

    WorkspaceReleasePipeline(ctx).run()