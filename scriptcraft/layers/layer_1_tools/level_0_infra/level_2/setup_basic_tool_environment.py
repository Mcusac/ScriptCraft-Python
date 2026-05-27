"""
Environment bootstrap helper for CLI-style tool entrypoints.
"""

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    cwd_indicators_basic,
    dev_project_root_from_file,
    get_environment_type_from_bool,
    is_distributable_from_cwd,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import setup_import_paths_common

__all__ = ["setup_basic_tool_environment"]


def setup_basic_tool_environment(
    *,
    file_path: str | Path,
    tool_dir_name: str,
    dev_levels_up: int = 5,
) -> bool:
    dev_root = dev_project_root_from_file(Path(file_path), levels_up=dev_levels_up)
    indicators = cwd_indicators_basic(tool_dir_name)

    is_distributable = is_distributable_from_cwd(indicators)

    setup_import_paths_common(
        is_distributable=is_distributable,
        dev_root=dev_root,
    )

    env_type = get_environment_type_from_bool(is_distributable)
    print(f"🔧 Environment: {env_type}")

    return is_distributable
