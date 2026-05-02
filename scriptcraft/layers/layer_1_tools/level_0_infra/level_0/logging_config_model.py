# level_0/logging_config_model.py

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union
import logging


def _normalize_level(level: Union[str, int]) -> int:
    """Normalize log level to logging int."""
    if isinstance(level, str):
        return getattr(logging, level.upper(), logging.INFO)
    return level


@dataclass
class LogConfigModel:
    """
    Pure configuration model for logging.

    No side effects. Safe to construct, copy, serialize, and load from external sources.
    """

    level: Union[str, int] = logging.INFO
    verbose_mode: bool = False
    structured_logging: bool = False
    use_timestamps: bool = True
    log_dir: Union[str, Path] = "logs"
    log_file: Optional[str] = None

    def normalize(self) -> "LogConfigModel":
        """
        Return a normalized copy with resolved types.
        """
        return LogConfigModel(
            level=_normalize_level(self.level),
            verbose_mode=self.verbose_mode,
            structured_logging=self.structured_logging,
            use_timestamps=self.use_timestamps,
            log_dir=Path(self.log_dir),
            log_file=self.log_file,
        )