"""
Logging handler factories.
"""

import logging
import sys
import datetime

from pathlib import Path


def _rotate_log(log_file: Path) -> None:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = log_file.with_suffix(f".{ts}{log_file.suffix}")
    try:
        log_file.rename(backup)
    except OSError:
        pass


def build_file_handler(log_file: Path, rotate: bool = True) -> logging.Handler:
    log_file.parent.mkdir(parents=True, exist_ok=True)

    if rotate and log_file.exists():
        _rotate_log(log_file)

    try:
        return logging.FileHandler(str(log_file), encoding="utf-8")
    except Exception:
        return logging.FileHandler(str(log_file))


def build_stream_handler() -> logging.Handler:
    try:
        return logging.StreamHandler(sys.stdout)
    except Exception:
        return logging.StreamHandler()


def configure_handler(
    handler: logging.Handler,
    level: int,
    formatter: logging.Formatter,
    logger: logging.Logger,
) -> None:
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def has_handler_type(logger: logging.Logger, handler_type: type) -> bool:
    return any(isinstance(h, handler_type) for h in logger.handlers)