from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from scriptcraft.layers.layer_0_core.level_1 import run_command


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def stringify_args(args: Sequence[str]) -> str:
    return " ".join(str(a) for a in args)


def python_module_args(module: str, *module_args: str) -> list[str]:
    return ["python", "-m", module, *module_args]


def python_file_args(path: str, *args: str) -> list[str]:
    return ["python", path, *args]


def run(
    args: Sequence[str],
    *,
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
) -> CommandResult:
    result = run_command(
        list(args),
        check=False,
        cwd=cwd,
        env=env,
    )
    return CommandResult(
        returncode=int(result["returncode"]),
        stdout=result.get("stdout") or "",
        stderr=result.get("stderr") or "",
    )

