"""Pure logging configuration model (no handler side effects)."""

import logging

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union


def normalize_level(level: Union[str, int]) -> int:
    """Normalize log level to logging int."""
    if isinstance(level, str):
        return getattr(logging, level.upper(), logging.INFO)
    return level


@dataclass
class LogConfigModel:
    """Configuration DTO for logging bootstrap."""

    level: Union[str, int] = logging.INFO
    verbose_mode: bool = False
    structured_logging: bool = False
    use_timestamps: bool = True
    log_dir: Union[str, Path] = "logs"
    log_file: Optional[str] = None

    def normalize(self) -> "LogConfigModel":
        return LogConfigModel(
            level=normalize_level(self.level),
            verbose_mode=self.verbose_mode,
            structured_logging=self.structured_logging,
            use_timestamps=self.use_timestamps,
            log_dir=Path(self.log_dir),
            log_file=self.log_file,
        )
