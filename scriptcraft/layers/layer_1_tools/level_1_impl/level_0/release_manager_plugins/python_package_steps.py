"""
Python-package release helpers.

These helpers are tool-specific (impl-level) but kept separate from the plugin
orchestration to reduce cognitive load and make the workflow more composable.
"""

import os

from pathlib import Path

from scriptcraft.layers.layer_0_core.level_1 import run_command

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import get_config
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print


def get_workspace_version_strategy() -> str:
  env_value = os.environ.get("WORKSPACE_VERSION_STRATEGY")
  if env_value:
    return env_value.strip().lower()

  try:
    config = get_config()
    if config is not None:
      framework_cfg = (
        config.get_framework_config()
        if hasattr(config, "get_framework_config")
        else None
      )
      packaging = getattr(framework_cfg, "packaging", None)
      if isinstance(packaging, dict):
        value = packaging.get("workspace_version_strategy")
        if isinstance(value, str) and value.strip():
          return value.strip().lower()
  except Exception:
    pass

  return "mirror"


def upload_to_pypi(submodule_dir: Path) -> bool:
  dist_dir = submodule_dir / "dist"
  files = list(dist_dir.glob("*.whl")) + list(dist_dir.glob("*.tar.gz"))
  if not files:
    log_and_print("❌ No distribution files found in dist/", level="error")
    return False

  log_and_print("🔍 Uploading to PyPI...")
  result = run_command(
    ["python", "-m", "twine", "upload", *[str(p) for p in files]],
    check=False,
    cwd=submodule_dir,
  )
  if int(result["returncode"]) == 0:
    log_and_print("✅ Uploading to PyPI - SUCCESS")
    return True

  log_and_print("❌ Uploading to PyPI - FAILED", level="error")
  stderr = (result.get("stderr") or "").strip()
  if stderr:
    log_and_print(f"Error: {stderr}", level="error")
  return False

