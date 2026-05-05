"""
Canonical subprocess runner (infra-level).

Goals:
- Single source of truth for subprocess execution
- Consistent UTF-8 handling (Windows-safe)
- Arg-list execution as the core (no shell by default)
- Thin convenience wrappers for common usage patterns
- Minimal, composable, and testable design
"""
import os
import subprocess
import sys

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print


# =========================
# Result Model (Unified)
# =========================

@dataclass(frozen=True)
class ProcessResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


# =========================
# Environment (Single Source)
# =========================

def _build_env(base: Optional[dict[str, str]] = None) -> dict[str, str]:
    env = dict(base or os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return env


# =========================
# Core Execution (NO LOGGING)
# =========================

def run(
    args: Sequence[str],
    *,
    cwd: Optional[Path] = None,
    env: Optional[dict[str, str]] = None,
) -> ProcessResult:
    """
    Core subprocess execution (arg-list based, no shell).

    This is the SINGLE execution primitive.
    No logging, no side-effects beyond process execution.
    """
    try:
        completed = subprocess.run(
            list(args),
            cwd=str(cwd) if cwd is not None else None,
            env=_build_env(env),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        return ProcessResult(
            returncode=completed.returncode,
            stdout=(completed.stdout or "").strip(),
            stderr=(completed.stderr or "").strip(),
        )
    except Exception as e:
        return ProcessResult(
            returncode=1,
            stdout="",
            stderr=str(e),
        )


# =========================
# Shell Adapter (Thin Wrapper)
# =========================

def run_shell(
    command: str,
    *,
    cwd: Optional[Path] = None,
    env: Optional[dict[str, str]] = None,
) -> ProcessResult:
    """
    Execute a shell command.

    Use ONLY when shell features are required.
    """
    return run(
        ["bash", "-lc", command] if os.name != "nt" else ["cmd", "/c", command],
        cwd=cwd,
        env=env,
    )


# =========================
# Logging Convenience Wrappers
# =========================

def run_ok(
    args: Sequence[str],
    description: str,
    *,
    cwd: Optional[Path] = None,
) -> bool:
    """
    Run command and return True/False with logging.
    """
    log_and_print(f"🔍 {description}...")
    result = run(args, cwd=cwd)

    if result.ok:
        log_and_print(f"✅ {description} - SUCCESS")
        return True

    log_and_print(f"❌ {description} - FAILED", level="error")
    if result.stderr:
        log_and_print(f"Error: {result.stderr}", level="error")
    return False


def run_str(
    args: Sequence[str],
    description: str,
    *,
    cwd: Optional[Path] = None,
) -> Optional[str]:
    """
    Run command and return stdout (or None) with logging.
    """
    log_and_print(f"🔄 {description}...")
    result = run(args, cwd=cwd)

    if result.ok:
        log_and_print(f"✅ {description} completed")
        return result.stdout

    log_and_print(f"❌ {description} failed", level="error")
    if result.stderr:
        log_and_print(f"Error output: {result.stderr}", level="error")
    return None


def run_shell_ok(
    command: str,
    description: str,
    *,
    cwd: Optional[Path] = None,
) -> bool:
    """
    Shell-based version of run_ok.
    """
    log_and_print(f"🔍 {description}...")
    result = run_shell(command, cwd=cwd)

    if result.ok:
        log_and_print(f"✅ {description} - SUCCESS")
        return True

    log_and_print(f"❌ {description} - FAILED", level="error")
    if result.stderr:
        log_and_print(f"Error: {result.stderr}", level="error")
    return False


def run_shell_str(
    command: str,
    description: str,
    *,
    cwd: Optional[Path] = None,
) -> Optional[str]:
    """
    Shell-based version of run_str.
    """
    log_and_print(f"🔄 {description}...")
    result = run_shell(command, cwd=cwd)

    if result.ok:
        log_and_print(f"✅ {description} completed")
        return result.stdout

    log_and_print(f"❌ {description} failed", level="error")
    if result.stderr:
        log_and_print(f"Error output: {result.stderr}", level="error")
    return None


# =========================
# Arg Builders (Moved from PyPI Tool)
# =========================

def python_module_args(module: str, *module_args: str) -> list[str]:
    """
    Build args for: python -m module ...
    """
    return [sys.executable, "-m", module, *module_args]


def python_file_args(file_path: str, *file_args: str) -> list[str]:
    """
    Build args for: python file.py ...
    """
    return [sys.executable, file_path, *file_args]


def stringify_args(args: Iterable[str]) -> str:
    """
    For logging/debugging only.
    """
    return " ".join(str(a) for a in args)