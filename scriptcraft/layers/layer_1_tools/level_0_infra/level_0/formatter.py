"""
Logging formatters.
"""

import logging


class Utf8Formatter(logging.Formatter):
    """Formatter that replaces un-encodable characters instead of raising."""

    def format(self, record: logging.LogRecord) -> str:
        try:
            return super().format(record)
        except UnicodeEncodeError:
            record.msg = str(record.msg).encode("ascii", "replace").decode()
            return super().format(record)


DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"