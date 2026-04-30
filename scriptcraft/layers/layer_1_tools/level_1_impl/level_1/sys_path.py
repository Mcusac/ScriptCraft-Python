"""
`sys.path` mutation utilities for dev vs distributable layouts.
"""

import sys

from pathlib import Path
from typing import Optional

from layers.layer_1_tools.level_1_impl.level_0.env.layout import resolve_distributable_base_dir


def ensure_sys_path(path: Path) -> None:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)


def setup_import_paths_common(
    *,
    is_distributable: bool,
    dev_root: Path,
    cwd: Optional[Path] = None,
) -> None:
    """
    Shared `sys.path` setup used by Pattern-A env modules.
    """
    if is_distributable:
        base_dir = resolve_distributable_base_dir(cwd=cwd)
        ensure_sys_path(base_dir)
        return

    ensure_sys_path(dev_root)

