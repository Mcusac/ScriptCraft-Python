
import subprocess


def list_submodules() -> list[str]:
    """
    Return submodule paths from `git submodule status`.

    Output lines look like:
      "<prefix><sha> <path> (<meta...>)"
    We extract the second whitespace-delimited token as the submodule path.
    """
    try:
        result = subprocess.run(
            ["git", "submodule", "status"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        return []

    if result.returncode != 0:
        return []

    lines = [ln for ln in result.stdout.splitlines() if ln.strip()]
    submodules: list[str] = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            submodules.append(parts[1])
    return submodules

