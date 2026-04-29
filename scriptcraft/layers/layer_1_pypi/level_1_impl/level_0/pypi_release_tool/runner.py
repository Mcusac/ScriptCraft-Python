from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable, Sequence

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


def _utf8_env(base: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(base or os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run_command(
    args: Sequence[str],
    *,
    description: str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
) -> CommandResult:
    log_and_print(f"🔍 {description}...")

    try:
        completed = subprocess.run(
            list(args),
            cwd=cwd,
            env=_utf8_env(env),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        return CommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
    except Exception as e:
        return CommandResult(returncode=1, stdout="", stderr=str(e))


def python_module_args(module: str, *module_args: str) -> list[str]:
    return [sys.executable, "-m", module, *module_args]


def python_file_args(file_path: str, *file_args: str) -> list[str]:
    return [sys.executable, file_path, *file_args]


def stringify_args(args: Iterable[str]) -> str:
    # For logging only; execution uses list-args to avoid quoting issues.
    return " ".join(str(a) for a in args)

