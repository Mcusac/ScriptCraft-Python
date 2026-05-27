"""Path resolution helpers for release-manager plugins."""

from pathlib import Path
from typing import Optional, Tuple

SUBMODULE_REL = Path("implementations") / "python-package"


def find_workspace_root(start: Optional[Path] = None) -> Path:
  """Locate workspace root by searching upward for config.yaml."""
  current = (start or Path.cwd()).resolve()
  for parent in [current, *current.parents]:
    if (parent / "config.yaml").exists():
      return parent
  return current


def resolve_python_package_paths(
  start: Optional[Path] = None,
) -> Tuple[Path, Path]:
  """
  Return (submodule_dir, workspace_root).

  If cwd is python-package, submodule_dir is cwd and workspace_root is two levels up.
  Otherwise submodule_dir is workspace/implementations/python-package when it exists.
  """
  original = (start or Path.cwd()).resolve()

  if original.name == "python-package":
    submodule_dir = original
    workspace_root = original.parent.parent
    return submodule_dir, workspace_root

  workspace_root = find_workspace_root(original)
  submodule_dir = workspace_root / SUBMODULE_REL
  if submodule_dir.exists():
    return submodule_dir, workspace_root

  fallback = original / SUBMODULE_REL
  if fallback.exists():
    return fallback, workspace_root

  return submodule_dir, workspace_root


def submodule_path(workspace_root: Path) -> Path:
  return workspace_root / SUBMODULE_REL
