"""
Logging formatters for different output formats and contexts.
"""

import logging
from typing import Optional


class QCFormatter(logging.Formatter):
    """Formatter for QC-specific logging with structured output."""

    def format(self, record: logging.LogRecord) -> str:
        if hasattr(record, "qc_context"):
            return f"[QC] {record.getMessage()}"
        return super().format(record)


class TimestampFormatter(logging.Formatter):
    """Formatter that prepends an ISO-style timestamp using the standard logging mechanism."""

    DEFAULT_FMT = "%(asctime)s — %(message)s"
    DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"

    def __init__(self) -> None:
        super().__init__(fmt=self.DEFAULT_FMT, datefmt=self.DEFAULT_DATEFMT)


class PlainFormatter(logging.Formatter):
    """Minimal formatter that emits only the message."""

    def __init__(self) -> None:
        super().__init__(fmt="%(message)s")


def create_formatter(
    log_format: Optional[str] = None,
    include_timestamp: bool = True,
    qc_format: bool = False,
) -> logging.Formatter:
    """
    Create a formatter with the specified options.

    Args:
        log_format: Custom format string; takes precedence when provided.
        include_timestamp: Use TimestampFormatter when no custom format is given.
        qc_format: Return a QCFormatter (highest precedence).

    Returns:
        Configured logging.Formatter instance.
    """
    if qc_format:
        return QCFormatter()
    if log_format:
        return logging.Formatter(log_format)
    if include_timestamp:
        return TimestampFormatter()
    return PlainFormatter()