"""Mutable logging bootstrap configuration (pre-controller)."""

import logging
from dataclasses import dataclass


@dataclass
class LogConfig:
    log_level: int = logging.INFO
    default_log_dir: str = "logs"
    verbose_mode: bool = False

    def set_verbose_mode(self, enabled: bool) -> None:
        self.verbose_mode = bool(enabled)
