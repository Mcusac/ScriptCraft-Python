"""
Logging emission utilities.
"""

import logging
from pathlib import Path
from typing import Dict


def _get_logger(name: str) -> logging.Logger:
    return logging.getLogger() if name == "root" else logging.getLogger(name)


def log(
    message: str,
    level: str = "info",
    logger_name: str = "root",
) -> None:
    logger = _get_logger(logger_name)
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message)


def print_message(message: str) -> None:
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("ascii", "replace").decode())


def log_and_print(
    message: str,
    level: str = "info",
    logger_name: str = "root",
    verbose: bool = True,
) -> None:
    log(message, level, logger_name)

    if verbose:
        print_message(message)


def get_handler_paths(logger_name: str = "root") -> Dict[str, Path]:
    """
    Return resolved paths of every FileHandler on the specified logger.

    Args:
        logger_name: Logger name ("root" for root logger)

    Returns:
        Mapping of resolved path string → Path object
    """
    logger = _get_logger(logger_name)

    return {
        str(Path(h.baseFilename).resolve()): Path(h.baseFilename)
        for h in logger.handlers
        if isinstance(h, logging.FileHandler)
    }