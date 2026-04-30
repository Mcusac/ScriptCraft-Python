"""
Environment Detection Module

This module provides environment detection and path/import helpers for the
RHQ Form Autofiller tool.
"""

from pathlib import Path

from layers.layer_1_tools.level_1_impl.level_0.env.layout import get_environment_type_from_bool
from layers.layer_1_tools.level_1_impl.level_1.sys_path import ensure_sys_path


def setup_environment() -> bool:
    """
    Complete environment setup - call this at the top of your main.py.
    
    Returns:
        True if in distributable environment, False if in development
    """
    current_file = Path(__file__).resolve()
    has_common_sibling = (current_file.parent / "common").exists()
    in_scripts_subdir = "scripts" in current_file.parts
    is_distributable = has_common_sibling or in_scripts_subdir

    if is_distributable:
        ensure_sys_path(current_file.parent)

    env_type = get_environment_type_from_bool(is_distributable)
    print(f"🔧 Environment: {env_type}")

    return is_distributable