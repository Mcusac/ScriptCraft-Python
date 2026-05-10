from pathlib import Path
from typing import Optional, Union

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1.environment_resolver import EnvironmentResolver
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6.argument_parsers import ArgumentValidator


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
        ArgumentValidator.ensure_output_dir(path)
        return path