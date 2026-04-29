"""
Semver helpers used by release tooling.
"""

from typing import Optional

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print


def bump_version(current_version: str, version_type: str) -> Optional[str]:
    """Bump version number based on type (major/minor/patch)."""
    try:
        major, minor, patch = map(int, current_version.split("."))
    except Exception:
        log_and_print(f"❌ Invalid current version format: {current_version}", level="error")
        return None

    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        log_and_print("❌ Invalid version type. Use: major, minor, or patch", level="error")
        return None

    return f"{major}.{minor}.{patch}"

