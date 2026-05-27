"""Git submodule path discovery primitives."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.git_service import GitService


def list_submodule_paths(*, git: GitService | None = None) -> list[str]:
    """Return repository submodule paths from `git submodule status`."""
    service = git or GitService()
    result = service._run_git("submodule status")
    if result.returncode != 0:
        return []

    submodules: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2:
            submodules.append(parts[1])
    return submodules
