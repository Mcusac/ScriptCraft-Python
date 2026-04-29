"""
Local composition helpers for level_1 tool env modules.

These helpers keep the env modules thin by wiring the shared primitives from
`layers.layer_1_pypi.level_1_impl.level_0.env_base` into a standard pattern.
"""

from pathlib import Path

from layers.layer_1_pypi.level_1_impl.level_0.env.cwd_indicators import cwd_indicators_basic, is_distributable_from_cwd
from layers.layer_1_pypi.level_1_impl.level_0.env.layout import dev_project_root_from_file, get_environment_type_from_bool
from layers.layer_1_pypi.level_1_impl.level_1.sys_path import setup_import_paths_common


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

