# level_0/structured_formatter.py

import json
import logging


class StructuredFormatter(logging.Formatter):
    """
    Formatter for structured JSON logging.
    """

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