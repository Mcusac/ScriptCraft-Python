"""
level_2/logging_context.py

Context managers and summary helpers for logging operations.
Consolidates QCLogContext, qc_log_context, with_domain_logger, and log_fix_summary.
"""

import contextlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Generator, Optional, TypeVar, Union

from layers.layer_1_tools.level_0_infra.level_1.logger_config import setup_logger

T = TypeVar("T")


# ── Class-based context manager ───────────────────────────────────────────────

class QCLogContext:
    """Class-style context manager for a single named QC operation."""

    def __init__(self, logger: logging.Logger, operation: str = "Unknown") -> None:
        self.logger = logger
        self.operation = operation
        self._start: datetime

    def __enter__(self) -> "QCLogContext":
        self._start = datetime.now()
        self.logger.info("Starting QC operation: %s", self.operation)
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        elapsed = (datetime.now() - self._start).total_seconds()
        if exc_type is None:
            self.logger.info(
                "Completed QC operation '%s' in %.2fs", self.operation, elapsed
            )
        else:
            self.logger.error(
                "QC operation '%s' failed after %.2fs: %s",
                self.operation,
                elapsed,
                exc_val,
            )


# ── Function-based context managers ──────────────────────────────────────────

@contextlib.contextmanager
def qc_log_context(
    log_path: Union[str, Path],
    operation: Optional[str] = None,
    **_context: Any,
) -> Generator[logging.Logger, None, None]:
    """
    Context manager for QC logging operations.

    Args:
        log_path:  Path to the log file (or an existing Logger).
        operation: Human-readable operation name for start/end messages.

    Yields:
        Configured Logger instance.
    """
    logger = setup_logger(log_file=log_path, clear_handlers=False)
    start = datetime.now()

    if operation:
        logger.info("Starting QC operation: %s", operation)

    try:
        yield logger
    except Exception as exc:
        elapsed = (datetime.now() - start).total_seconds()
        if operation:
            logger.error(
                "QC operation '%s' failed after %.2fs: %s", operation, elapsed, exc
            )
        raise
    else:
        elapsed = (datetime.now() - start).total_seconds()
        if operation:
            logger.info(
                "Completed QC operation '%s' in %.2fs", operation, elapsed
            )


@contextlib.contextmanager
def with_domain_logger(
    log_path: Union[str, Path],
    func: Callable[[], T],
) -> Generator[None, None, None]:
    """
    Run *func* inside a timed, logged context and then yield.

    Args:
        log_path: Path to the log file.
        func:     Zero-argument callable to execute before yielding.
    """
    logger = setup_logger(log_file=log_path, clear_handlers=False)
    start = datetime.now()
    logger.info("Starting domain operation")
    try:
        func()
        yield
    except Exception as exc:
        elapsed = (datetime.now() - start).total_seconds()
        logger.error("Domain operation failed after %.2fs: %s", elapsed, exc)
        raise
    else:
        elapsed = (datetime.now() - start).total_seconds()
        logger.info("Completed domain operation in %.2fs", elapsed)


# ── Summary helpers ───────────────────────────────────────────────────────────

def log_fix_summary(
    logger: logging.Logger,
    fixes: Dict[str, Any],
    total_items: Optional[int] = None,
) -> None:
    """
    Log a human-readable fix summary.

    Args:
        logger:      Logger to write to.
        fixes:       Mapping of fix-type → count (int) or nested dict.
        total_items: Optional total item count to append.
    """
    if not fixes:
        logger.info("No fixes applied.")
        return

    logger.info("Fix Summary:")
    for key, value in fixes.items():
        if isinstance(value, dict):
            logger.info("  %s:", key)
            for subkey, subval in value.items():
                logger.info("    %s: %s", subkey, subval)
        else:
            logger.info("  %s: %s", key, value)

    if total_items is not None:
        logger.info("Total items processed: %d", total_items)