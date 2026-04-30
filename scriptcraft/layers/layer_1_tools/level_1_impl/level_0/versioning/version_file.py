"""
Read/write version file helpers.
"""

import re

from pathlib import Path
from typing import Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print


def get_current_version(*, version_file: Path = Path("scriptcraft/_version.py")) -> Optional[str]:
    """Get current version from a `_version.py` file."""
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'__version__ = "([^"]+)"', content)
            if match:
                return match.group(1)
        log_and_print("❌ Could not find version in _version.py", level="error")
        return None
    except FileNotFoundError:
        log_and_print("❌ _version.py file not found", level="error")
        return None


def update_version_file(
    new_version: str,
    *,
    version_file: Path = Path("scriptcraft/_version.py"),
    pyproject_file: Optional[Path] = Path("pyproject.toml"),
) -> bool:
    """Update the `_version.py` file (and optionally `pyproject.toml`) with a new version."""
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            content = f.read()

        updated_content = re.sub(
            r'__version__ = "[^"]+"',
            f'__version__ = "{new_version}"',
            content,
        )

        with open(version_file, "w", encoding="utf-8") as f:
            f.write(updated_content)

        log_and_print(f"✅ Updated _version.py to {new_version}")
        if pyproject_file is not None:
            if not update_pyproject_version(new_version, pyproject_file=pyproject_file):
                return False
        return True
    except Exception as e:
        log_and_print(f"❌ Error updating _version.py: {e}", level="error")
        return False


def get_pyproject_version(*, pyproject_file: Path = Path("pyproject.toml")) -> Optional[str]:
    """Get version from `pyproject.toml` \(`project.version`\)."""
    try:
        content = pyproject_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        log_and_print("❌ pyproject.toml not found", level="error")
        return None
    except Exception as e:
        log_and_print(f"❌ Error reading pyproject.toml: {e}", level="error")
        return None

    project_block = _extract_toml_table(content, "project")
    if not project_block:
        log_and_print("❌ Could not find [project] in pyproject.toml", level="error")
        return None

    match = re.search(r'(?m)^\s*version\s*=\s*"([^"]+)"\s*$', project_block)
    if match:
        return match.group(1)

    return None


def update_pyproject_version(
    new_version: str,
    *,
    pyproject_file: Path = Path("pyproject.toml"),
) -> bool:
    """Update `pyproject.toml` to use a static `project.version`."""
    try:
        content = pyproject_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        log_and_print("❌ pyproject.toml not found", level="error")
        return False
    except Exception as e:
        log_and_print(f"❌ Error reading pyproject.toml: {e}", level="error")
        return False

    updated = content
    updated = _ensure_project_version(updated, new_version)
    updated = _remove_dynamic_version(updated)
    updated = _remove_setuptools_dynamic_version_attr(updated)

    try:
        pyproject_file.write_text(updated, encoding="utf-8")
    except Exception as e:
        log_and_print(f"❌ Error writing pyproject.toml: {e}", level="error")
        return False

    log_and_print(f"✅ Updated pyproject.toml to version {new_version}")
    return True


def _extract_toml_table(content: str, table: str) -> Optional[str]:
    pattern = re.compile(
        rf"(?ms)^\[{re.escape(table)}\]\s*$\n(.*?)(?=^\[[^\]]+\]\s*$|\Z)"
    )
    match = pattern.search(content)
    return match.group(1) if match else None


def _ensure_project_version(content: str, new_version: str) -> str:
    pattern = re.compile(
        r'(?ms)^\[project\]\s*$\n(?P<body>.*?)(?=^\[[^\]]+\]\s*$|\Z)'
    )
    match = pattern.search(content)
    if not match:
        log_and_print("❌ Could not find [project] in pyproject.toml", level="error")
        return content

    body = match.group("body")
    if re.search(r'(?m)^\s*version\s*=\s*".*?"\s*$', body):
        body = re.sub(
            r'(?m)^\s*version\s*=\s*".*?"\s*$',
            f'version = "{new_version}"',
            body,
        )
    else:
        insert_at = 0
        name_match = re.search(r"(?m)^\s*name\s*=\s*\"[^\"]+\"\s*$\n?", body)
        if name_match:
            insert_at = name_match.end(0)
        body = body[:insert_at] + f'version = "{new_version}"\n' + body[insert_at:]

    return content[: match.start("body")] + body + content[match.end("body") :]


def _remove_dynamic_version(content: str) -> str:
    """Remove `version` from `project.dynamic` if present."""
    pattern = re.compile(
        r'(?ms)^\[project\]\s*$\n(?P<body>.*?)(?=^\[[^\]]+\]\s*$|\Z)'
    )
    match = pattern.search(content)
    if not match:
        return content

    body = match.group("body")
    dyn_match = re.search(r"(?ms)^\s*dynamic\s*=\s*\[(?P<list>.*?)\]\s*$", body)
    if not dyn_match:
        return content

    items = re.findall(r'"([^"]+)"', dyn_match.group("list"))
    kept = [i for i in items if i != "version"]

    if not kept:
        body = re.sub(r"(?ms)^\s*dynamic\s*=\s*\[.*?\]\s*$\n?", "", body)
    else:
        new_list = ", ".join(f'"{i}"' for i in kept)
        body = re.sub(
            r"(?ms)^\s*dynamic\s*=\s*\[.*?\]\s*$",
            f"dynamic = [{new_list}]",
            body,
        )

    return content[: match.start("body")] + body + content[match.end("body") :]


def _remove_setuptools_dynamic_version_attr(content: str) -> str:
    """Drop `[tool.setuptools.dynamic] version = {attr = ...}` if present."""
    pattern = re.compile(
        r'(?ms)^\[tool\.setuptools\.dynamic\]\s*$\n(?P<body>.*?)(?=^\[[^\]]+\]\s*$|\Z)'
    )
    match = pattern.search(content)
    if not match:
        return content

    body = match.group("body")
    body_updated = re.sub(
        r'(?m)^\s*version\s*=\s*\{[^}]*\}\s*$\n?',
        "",
        body,
    ).rstrip()

    if not body_updated:
        return content[: match.start(0)] + content[match.end(0) :]

    body_updated = body_updated + "\n"
    return content[: match.start("body")] + body_updated + content[match.end("body") :]

