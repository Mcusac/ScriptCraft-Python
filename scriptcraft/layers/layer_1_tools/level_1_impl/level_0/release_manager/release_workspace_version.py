"""Workspace VERSION and CHANGELOG helpers for workspace release."""

import re

from datetime import datetime
from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print


def get_current_workspace_version() -> str | None:
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
    except Exception as exc:
        log_and_print(f"❌ Error updating VERSION file: {exc}", level="error")
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


def update_changelog(new_version: str, version_type: str) -> bool:
    _ = version_type
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
    except Exception as exc:
        log_and_print(f"❌ Error updating CHANGELOG.md: {exc}", level="error")
        return False
