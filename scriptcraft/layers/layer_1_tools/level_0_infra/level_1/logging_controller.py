# level_1/logging_controller.py

import logging
from pathlib import Path
from typing import Union

from layers.layer_1_tools.level_0_infra.level_0.logging_config_model import LogConfigModel
from layers.layer_1_tools.level_0_infra.level_0.structured_formatter import StructuredFormatter


class LogController:
    """
    Centralized logging controller.

    Responsible for:
    - Applying configuration to Python logging
    - Managing formatter lifecycle
    - Updating handlers

    This is the ONLY place where logging side effects occur.
    """

    def __init__(self, config: LogConfigModel) -> None:
        self.config = config.normalize()
        self.formatter: logging.Formatter = logging.Formatter()
        self._apply_all()

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _build_formatter(self) -> logging.Formatter:
        if self.config.structured_logging:
            return StructuredFormatter(self.config.use_timestamps)

        fmt = (
            "%(asctime)s — %(levelname)s — %(message)s"
            if self.config.use_timestamps
            else "%(levelname)s — %(message)s"
        )

        datefmt = "%Y-%m-%d %H:%M:%S" if self.config.use_timestamps else None
        return logging.Formatter(fmt, datefmt)

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

    # ── Public API (controlled mutations) ────────────────────────────────────

    def set_timestamps(self, enabled: bool) -> None:
        self.config.use_timestamps = enabled
        self._apply_formatter()

    def set_log_level(self, level: Union[str, int]) -> None:
        from .logging_config_model import _normalize_level

        self.config.level = _normalize_level(level)
        self._apply_log_level()

    def set_structured_logging(self, enabled: bool) -> None:
        self.config.structured_logging = enabled
        self._apply_formatter()

    def set_verbose_mode(self, enabled: bool) -> None:
        self.config.verbose_mode = enabled

    def set_log_dir(self, path: Union[str, Path]) -> None:
        self.config.log_dir = Path(path)
        self._ensure_log_dir()

    # ── Explicit apply (important for clarity) ───────────────────────────────

    def apply(self) -> None:
        """
        Explicitly reapply full configuration.
        Useful if config was mutated externally.
        """
        self._apply_all()