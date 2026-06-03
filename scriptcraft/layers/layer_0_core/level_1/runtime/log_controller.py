"""
Mutable root-logger controller driven by LogConfigModel.

``setup_logging`` in ``level_0.runtime.log_configure`` is the minimal idempotent
bootstrap. ``LogController`` applies a normalized ``LogConfigModel`` to the root
logger (level, formatters, log directory) for framework configuration.
"""

import logging

from pathlib import Path
from typing import Union

from scriptcraft.layers.layer_0_core.level_0.runtime.formatters import (
    StructuredFormatter,
    Utf8Formatter,
)
from scriptcraft.layers.layer_0_core.level_0.runtime.logging_config_model import (
    LogConfigModel,
    normalize_level,
)


class LogController:
    """
    Centralized logging controller.

    Responsible for:
    - Applying configuration to Python logging
    - Managing formatter lifecycle
    - Updating handlers
    """

    def __init__(self, config: LogConfigModel) -> None:
        self.config = config.normalize()
        self.formatter: logging.Formatter = logging.Formatter()
        self._apply_all()

    def _build_formatter(self) -> logging.Formatter:
        if self.config.structured_logging:
            return StructuredFormatter(self.config.use_timestamps)

        fmt = (
            "%(asctime)s — %(levelname)s — %(message)s"
            if self.config.use_timestamps
            else "%(levelname)s — %(message)s"
        )

        datefmt = "%Y-%m-%d %H:%M:%S" if self.config.use_timestamps else None
        return Utf8Formatter(fmt, datefmt=datefmt)

    def _apply_formatter(self) -> None:
        self.formatter = self._build_formatter()
        for handler in logging.getLogger().handlers:
            handler.setFormatter(self.formatter)

    def _apply_log_level(self) -> None:
        logging.getLogger().setLevel(self.config.level)

    def _ensure_log_dir(self) -> None:
        Path(self.config.log_dir).mkdir(parents=True, exist_ok=True)

    def _apply_all(self) -> None:
        self._ensure_log_dir()
        self._apply_log_level()
        self._apply_formatter()

    def set_timestamps(self, enabled: bool) -> None:
        self.config.use_timestamps = enabled
        self._apply_formatter()

    def set_log_level(self, level: Union[str, int]) -> None:
        self.config.level = normalize_level(level)
        self._apply_log_level()

    def set_structured_logging(self, enabled: bool) -> None:
        self.config.structured_logging = enabled
        self._apply_formatter()

    def set_verbose_mode(self, enabled: bool) -> None:
        self.config.verbose_mode = enabled

    def set_log_dir(self, path: Union[str, Path]) -> None:
        self.config.log_dir = Path(path)
        self._ensure_log_dir()

    def apply(self) -> None:
        """Reapply full configuration after external config mutation."""
        self._apply_all()
