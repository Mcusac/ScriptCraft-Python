import logging

from abc import ABC, abstractmethod
from typing import Any, List, Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    ValidationMixin,
    ErrorHandlingMixin,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    IOMixin,
    LoggingMixin,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import EnvironmentMixin
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import ConfigMixin


class BaseTool(
    ConfigMixin,
    LoggingMixin,
    EnvironmentMixin,
    ValidationMixin,
    IOMixin,
    ErrorHandlingMixin,
    ABC,
):
    """Composed base tool with separated concerns."""

    def __init__(
        self,
        name: str,
        description: str,
        supported_formats: Optional[List[str]] = None,
        tool_name: Optional[str] = None,
        requires_dictionary: bool = False,
    ) -> None:
        self.name = name
        self.description = description
        self.logger = logging.getLogger(name)

        self.supported_formats = supported_formats or ['.csv', '.xlsx', '.xls']
        self.requires_dictionary = requires_dictionary
        self.tool_name = tool_name or name.lower().replace(' ', '_')

        self._config = None  # used by ConfigMixin

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        pass