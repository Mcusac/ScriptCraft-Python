"""Logging formatters shared across tools and core."""

import json
import logging

DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

class Utf8Formatter(logging.Formatter):
    """Formatter that replaces un-encodable characters instead of raising."""

    def format(self, record: logging.LogRecord) -> str:
        try:
            return super().format(record)
        except UnicodeEncodeError:
            record.msg = str(record.msg).encode("ascii", "replace").decode()
            return super().format(record)


class StructuredFormatter(logging.Formatter):
    """Formatter for structured JSON logging."""

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
