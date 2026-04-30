"""
Core logging: formatter, logger setup, and message emission.

Keep this module minimal. It must not import from any other
level_0_infra module to avoid circular dependencies.
"""

import logging
import sys
import datetime

from pathlib import Path
from typing import Any, Dict, List, Optional, Union


# ── UTF-8-safe formatter ─────────────────────────────────────────────────────

class Utf8Formatter(logging.Formatter):
    """Formatter that replaces un-encodable characters instead of raising."""

    def format(self, record: logging.LogRecord) -> str:
        try:
            return super().format(record)
        except UnicodeEncodeError:
            record.msg = str(record.msg).encode("ascii", "replace").decode()
            return super().format(record)


# ── Private helpers ───────────────────────────────────────────────────────────

def _rotate_log(log_file: Path) -> None:
    """Rename an existing log file with a timestamp suffix."""
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = log_file.with_suffix(f".{ts}{log_file.suffix}")
    try:
        log_file.rename(backup)
    except OSError:
        pass  # Non-fatal; proceed without rotation.


def _add_file_handler(
    logger: logging.Logger,
    log_file: Path,
    level: int,
    formatter: logging.Formatter,
    rotate: bool,
) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    if rotate and log_file.exists():
        _rotate_log(log_file)
    try:
        handler = logging.FileHandler(str(log_file), encoding="utf-8")
    except Exception:
        handler = logging.FileHandler(str(log_file))
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def _add_stream_handler(
    logger: logging.Logger,
    level: int,
    formatter: logging.Formatter,
) -> None:
    try:
        handler = logging.StreamHandler(sys.stdout)
    except Exception:
        handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def _has_handler_type(logger: logging.Logger, handler_type: type) -> bool:
    return any(isinstance(h, handler_type) for h in logger.handlers)


# ── Public API ────────────────────────────────────────────────────────────────

DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Emoji prefixes keyed by log level name (lower-case).
_LEVEL_EMOJI: Dict[str, str] = {
    "debug":    "🔍 ",
    "info":     "📝 ",
    "warning":  "⚠️ ",
    "error":    "❌ ",
    "critical": "💥 ",
}
_KNOWN_EMOJIS = frozenset("🔍📝⚠️❌💥🚀✅🎯📊📁🔧💡🎉🏁")


def _prefix_message(message: str, level: str) -> str:
    """Prepend a level emoji if the message does not already start with one."""
    if not any(ch in message[:3] for ch in _KNOWN_EMOJIS):
        return _LEVEL_EMOJI.get(level.lower(), "") + message
    return message


def log_and_print(
    message: str,
    level: str = "info",
    logger_name: str = "root",
    verbose: bool = True,
) -> None:
    """
    Log *message* and, when *verbose* is True, print it to stdout.

    Args:
        message:     Text to log.
        level:       Logging level string (``"info"``, ``"warning"``, etc.).
        logger_name: Name of the target logger.
        verbose:     Whether to also print to stdout.
    """
    message = _prefix_message(message, level)
    logger = logging.getLogger(logger_name) if logger_name != "root" else logging.getLogger()
    getattr(logger, level.lower(), logger.info)(message)

    if verbose:
        try:
            print(message)
        except UnicodeEncodeError:
            print(message.encode("ascii", "replace").decode())


def setup_logger(
    name: str = "root",
    level: Union[str, int] = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    log_format: str = DEFAULT_LOG_FORMAT,
    verbose: bool = True,
    clear_handlers: bool = True,
    rotate_logs: bool = True,
) -> logging.Logger:
    """
    Configure and return a logger.

    Args:
        name:           Logger name; ``"root"`` targets the root logger.
        level:          Log level as a string (``"INFO"``) or integer.
        log_file:       Optional path for a file handler.
        log_format:     Format string passed to the formatter.
        verbose:        When True, add a stream handler if one is absent.
        clear_handlers: When True, remove existing handlers before adding new ones.
        rotate_logs:    When True, rename an existing *log_file* before opening.

    Returns:
        The configured ``logging.Logger``.
    """
    logger = logging.getLogger(name) if name != "root" else logging.getLogger()

    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(level)

    if clear_handlers:
        logger.handlers.clear()

    formatter = Utf8Formatter(log_format)

    if log_file and not _has_handler_type(logger, logging.FileHandler):
        _add_file_handler(logger, Path(log_file), level, formatter, rotate_logs)

    if verbose and not _has_handler_type(logger, logging.StreamHandler):
        _add_stream_handler(logger, level, formatter)

    if name != "root":
        logger.propagate = False

    return logger


def clear_handlers(logger_name: str = "root") -> None:
    """Remove all handlers from the named logger."""
    logging.getLogger(logger_name).handlers.clear()


def get_handler_paths(logger_name: str = "root") -> List[str]:
    """Return file paths of all FileHandler instances on the named logger."""
    logger = logging.getLogger(logger_name)
    return [
        h.baseFilename
        for h in logger.handlers
        if isinstance(h, logging.FileHandler)
    ]


# ── Display utility (belongs in a higher-level module; kept for compatibility) ─

def log_fix_summary(fixes: Dict[str, Any]) -> None:
    """
    Log a structured summary of applied fixes.

    NOTE: This is a display utility, not a core logging primitive.
    It should be migrated to a higher-level reporting module.
    """
    if not fixes:
        log_and_print("ℹ️ No fixes were applied.")
        return

    log_and_print("\n📊 Fix Summary:")
    for key, value in fixes.items():
        if isinstance(value, dict):
            log_and_print(f"  - {key}:")
            for sub_key, sub_val in value.items():
                log_and_print(f"    - {sub_key}: {sub_val}")
        else:
            log_and_print(f"  - {key}: {value}")