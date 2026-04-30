from __future__ import annotations

from layers.layer_1_tools.level_0_infra.level_0.directory_ops import get_domain_paths, get_project_root

PROJECT_ROOT = get_project_root()
DOMAIN_PATHS = get_domain_paths(PROJECT_ROOT)

