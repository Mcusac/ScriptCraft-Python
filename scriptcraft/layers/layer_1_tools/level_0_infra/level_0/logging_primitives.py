import logging
import json

from pathlib import Path
from typing import Union


class StructuredFormatter(logging.Formatter):
    def __init__(self, use_timestamps: bool = True) -> None:
        super().__init__()
        self.use_timestamps = use_timestamps

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }

        if self.use_timestamps:
            log_data["timestamp"] = self.formatTime(record)

        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)

        return json.dumps(log_data)


class LogConfig:
    def __init__(self, log_level: int, default_log_dir: Union[str, Path]) -> None:
        self.use_timestamps = True
        self.log_level = log_level
        self.verbose_mode = True
        self.use_structured_logging = False
        self.default_log_dir = Path(default_log_dir)
        self.formatter: logging.Formatter = logging.Formatter()
        self._update_formatter()

    def _update_formatter(self) -> None:
        if self.use_structured_logging:
            self.formatter = StructuredFormatter(self.use_timestamps)
        else:
            self.formatter = logging.Formatter(
                "%(asctime)s — %(levelname)s — %(message)s"
                if self.use_timestamps
                else "%(levelname)s — %(message)s",
                "%Y-%m-%d %H:%M:%S" if self.use_timestamps else None,
            )

    def set_timestamps(self, enabled: bool) -> None:
        self.use_timestamps = enabled
        self._update_formatter()
        self._update_all_handlers()

    def set_log_level(self, level: Union[str, int]) -> None:
        if isinstance(level, str):
            self.log_level = getattr(logging, level.upper(), logging.INFO)
        else:
            self.log_level = level
        logging.getLogger().setLevel(self.log_level)

    def set_structured_logging(self, enabled: bool) -> None:
        self.use_structured_logging = enabled
        self._update_formatter()
        self._update_all_handlers()

    def set_verbose_mode(self, enabled: bool) -> None:
        self.verbose_mode = enabled

    def set_default_log_dir(self, path: Union[str, Path]) -> None:
        self.default_log_dir = Path(path)
        self.default_log_dir.mkdir(parents=True, exist_ok=True)

    def _update_all_handlers(self) -> None:
        logger = logging.getLogger()
        for handler in logger.handlers:
            handler.setFormatter(self.formatter)