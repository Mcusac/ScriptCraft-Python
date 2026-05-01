"""
level_2/log_handlers.py

Handler introspection and attachment utilities.
Depends only on level_0 (handlers.py) and level_1 (logger_config.py).

clear_handlers lives at level_1/logger_config.py — import from there, never re-declare.
"""

import logging
from pathlib import Path
from typing import Dict, Union

from layers.layer_1_tools.level_0_infra.level_0.formatter import DEFAULT_LOG_FORMAT, Utf8Formatter
from layers.layer_1_tools.level_0_infra.level_0.handlers import (
    build_file_handler,
    configure_handler,
)


def get_handler_paths() -> Dict[str, Path]:
    """
    Return resolved paths of every FileHandler on the root logger.

    Returns:
        Mapping of resolved path string → Path object.
    """
    return {
        str(Path(h.baseFilename).resolve()): Path(h.baseFilename)
        for h in logging.getLogger().handlers
        if isinstance(h, logging.FileHandler)
    }


def add_file_handler(
    logger_name: str,
    log_file: Union[str, Path],
    level: Union[str, int] = "INFO",
    log_format: str = DEFAULT_LOG_FORMAT,
) -> None:
    """
    Attach a single FileHandler to an existing logger without disturbing
    its other handlers.  Use setup_logger when you need full initialisation.

    Args:
        logger_name: Target logger name ("root" for root logger).
        log_file:    Destination file path (parent dirs created if absent).
        level:       Handler log level (string or int).
        log_format:  Record format string.
    """
    logger = (
        logging.getLogger()
        if logger_name == "root"
        else logging.getLogger(logger_name)
    )

    numeric_level = (
        getattr(logging, level.upper(), logging.INFO)
        if isinstance(level, str)
        else level
    )

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    handler = build_file_handler(log_path, rotate_logs=True)
    configure_handler(handler, numeric_level, Utf8Formatter(log_format), logger)

    logger.info("Added file handler: %s", log_path)