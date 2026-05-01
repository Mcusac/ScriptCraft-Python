"""
Logger configuration.
"""

import logging

from pathlib import Path
from typing import Optional, Union

from layers.layer_1_tools.level_0_infra.level_0.formatter import Utf8Formatter, DEFAULT_LOG_FORMAT
from layers.layer_1_tools.level_0_infra.level_0.handlers import (
    build_file_handler,
    build_stream_handler,
    configure_handler,
    has_handler_type,
)


def _get_logger(name: str) -> logging.Logger:
    return logging.getLogger() if name == "root" else logging.getLogger(name)


def _normalize_level(level: Union[str, int]) -> int:
    if isinstance(level, str):
        return getattr(logging, level.upper(), logging.INFO)
    return level


def setup_logger(
    name: str = "root",
    level: Union[str, int] = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    log_format: str = DEFAULT_LOG_FORMAT,
    verbose: bool = True,
    clear_handlers: bool = True,
    rotate_logs: bool = True,
) -> logging.Logger:
    logger = _get_logger(name)

    level = _normalize_level(level)
    logger.setLevel(level)

    if clear_handlers:
        logger.handlers.clear()

    formatter = Utf8Formatter(log_format)

    if log_file and not has_handler_type(logger, logging.FileHandler):
        handler = build_file_handler(Path(log_file), rotate_logs)
        configure_handler(handler, level, formatter, logger)

    if verbose and not has_handler_type(logger, logging.StreamHandler):
        handler = build_stream_handler()
        configure_handler(handler, level, formatter, logger)

    if name != "root":
        logger.propagate = False

    return logger


def clear_handlers(logger_name: str = "root") -> None:
    _get_logger(logger_name).handlers.clear()