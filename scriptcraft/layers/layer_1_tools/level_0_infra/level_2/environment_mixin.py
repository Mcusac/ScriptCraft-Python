from pathlib import Path
from typing import Optional, Union

from layers.layer_1_tools.level_0_infra.level_0.directory_ops import ensure_output_dir
from layers.layer_1_tools.level_0_infra.level_1.environment_resolver import EnvironmentResolver


class EnvironmentMixin:
    """Handles environment + directory resolution."""

    def resolve_input_directory(
        self,
        input_dir: Optional[Union[str, Path]] = None,
    ) -> Path:
        return EnvironmentResolver.resolve_input_directory(input_dir, self.config)

    def resolve_output_directory(
        self,
        output_dir: Optional[Union[str, Path]] = None,
    ) -> Path:
        path = EnvironmentResolver.resolve_output_directory(output_dir, self.config)
        ensure_output_dir(path)
        return path