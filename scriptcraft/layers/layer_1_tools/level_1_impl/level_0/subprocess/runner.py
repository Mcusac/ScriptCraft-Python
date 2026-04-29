"""
Shared subprocess runner with a consistent UTF-8 policy.

We centralize encoding/env handling here to avoid Windows Unicode decode issues
and to keep command execution behavior consistent across tools.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print


@dataclass(frozen=True)
class RunResult:
    ok: bool
    returncode: int
    stdout: str
    stderr: str


def _build_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _run(
    command: str,
    *,
    cwd: Optional[Path] = None,
    check: bool,
) -> RunResult:
    try:
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=_build_env(),
            cwd=str(cwd) if cwd is not None else None,
            check=check,
        )
        return RunResult(
            ok=completed.returncode == 0,
            returncode=completed.returncode,
            stdout=(completed.stdout or "").strip(),
            stderr=(completed.stderr or "").strip(),
        )
    except subprocess.CalledProcessError as e:
        return RunResult(
            ok=False,
            returncode=e.returncode,
            stdout=(e.stdout or "").strip() if isinstance(e.stdout, str) else "",
            stderr=(e.stderr or "").strip() if isinstance(e.stderr, str) else "",
        )


def run_str(command: str, description: str, *, cwd: Optional[Path] = None) -> Optional[str]:
    """
    Run a command and return stdout (trimmed), or None on failure.
    """
    log_and_print(f"🔄 {description}...")
    result = _run(command, cwd=cwd, check=True)
    if result.ok:
        log_and_print(f"✅ {description} completed")
        return result.stdout

    log_and_print(f"❌ {description} failed", level="error")
    if result.stderr:
        log_and_print(f"Error output: {result.stderr}", level="error")
    return None


def run_ok(command: str, description: str, *, cwd: Optional[Path] = None) -> bool:
    """
    Run a command and return True on success, False otherwise.
    """
    log_and_print(f"🔍 {description}...")
    result = _run(command, cwd=cwd, check=False)
    if result.ok:
        log_and_print(f"✅ {description} - SUCCESS")
        return True

    log_and_print(f"❌ {description} - FAILED", level="error")
    if result.stderr:
        log_and_print(f"Error: {result.stderr}", level="error")
    return False

