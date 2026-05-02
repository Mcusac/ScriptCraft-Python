"""
Environment-aware path resolution utilities.

Centralizes logic for resolving input/output directories
based on runtime environment.
"""

from pathlib import Path
from typing import Optional, Union, Any

from layers.layer_1_tools.level_0_infra.level_0.environment import detect_environment
from layers.layer_1_tools.level_0_infra.level_1.config_accessors import get_template_config


class EnvironmentResolver:
    """Resolves filesystem paths based on runtime environment."""

    @staticmethod
    def is_production() -> bool:
        return detect_environment() == "production"

    @classmethod
    def resolve_input_directory(
        cls,
        input_dir: Optional[Union[str, Path]] = None,
        config: Optional[Any] = None,
    ) -> Path:
        if input_dir:
            return Path(input_dir)

        if config and hasattr(config, "paths") and hasattr(config.paths, "input_dir"):
            return Path(config.paths.input_dir)

        cwd = Path.cwd()

        if cls.is_production():
            return cwd.parent / "input" if cwd.name == "scripts" else cwd / "input"

        return Path("input")

    @classmethod
    def resolve_output_directory(
        cls,
        output_dir: Optional[Union[str, Path]] = None,
        config: Optional[Any] = None,
    ) -> Path:
        if output_dir:
            return Path(output_dir)

        # ---- Config-driven resolution ----
        if config:
            try:
                # Workspace config
                workspace = config.get_workspace_config()
                if workspace and hasattr(workspace, "paths"):
                    paths = workspace.paths
                    if isinstance(paths, dict) and "output_dir" in paths:
                        return Path(paths["output_dir"])

                # Template fallback (RESTORED)
                template = get_template_config(config)
                default_dir = (
                    template.get("package_structure", {})
                    .get("default_output_dir")
                )
                if isinstance(default_dir, str):
                    return Path(default_dir)

            except Exception:
                pass

        # ---- Environment fallback ----
        cwd = Path.cwd()

        if cls.is_production():
            return cwd.parent / "output" if cwd.name == "scripts" else cwd / "output"

        return Path("data/output")