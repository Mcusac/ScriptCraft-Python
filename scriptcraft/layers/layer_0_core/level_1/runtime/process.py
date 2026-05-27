"""Subprocess execution utilities.

Pure process execution without logging or printing side effects.
"""

import subprocess

from pathlib import Path
from typing import List, Optional, Mapping

from scriptcraft.layers.layer_0_core.level_0 import ProcessResult, validate_command


def run_command(
    cmd: List[str],
    check: bool = True,
    timeout: Optional[int] = None,
    cwd: Optional[Path] = None,
    env: Optional[Mapping[str, str]] = None,
) -> ProcessResult:
    """
    Execute a command.

    Args:
        cmd: Command as list of strings
        check: Raise CalledProcessError on failure
        timeout: Optional timeout in seconds
        cwd: Optional working directory
        env: Optional environment overrides (full environment mapping)

    Returns:
        ProcessResult
    """
    validate_command(cmd)

    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd is not None else None,
        env=dict(env) if env is not None else None,
        capture_output=True,
        text=True,
        check=check,
        timeout=timeout,
    )

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }