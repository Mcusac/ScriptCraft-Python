import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

from layers.layer_1_tools.level_0_infra.level_1.logger_config import setup_logger
from layers.layer_1_tools.level_0_infra.level_1.paths import LOG_LEVEL
from layers.layer_1_tools.level_0_infra.level_2.logging_bootstrap import build_log_config


# ============================================================
# 🌍 GLOBAL CONFIG (BOOTSTRAPPED)
# ============================================================

config = build_log_config()


# ============================================================
# 🧰 UTILITIES
# ============================================================

def clear_handlers(logger: Optional[logging.Logger] = None) -> None:
    logger = logger or logging.getLogger()
    while logger.handlers:
        logger.removeHandler(logger.handlers[0])


# ============================================================
# 📝 CORE LOGGING
# ============================================================

def log_message(
    message: str,
    level: str = "info",
    logger_name: str = "root",
    verbose: bool = True,
) -> None:
    setup_logger(
        message,
        level=level,
        logger_name=logger_name,
        verbose=verbose,
    )


# ============================================================
# 📁 FILE LOGGING UTILITIES
# ============================================================

def setup_logging_with_timestamp(
    log_dir: Path,
    mode: str,
    clear_handlers: bool = False,
) -> Path:
    """
    Creates a timestamped log file and initializes logging.
    """
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"{mode}_{timestamp}.log"

    setup_logger(
        log_file=log_file,
        level=LOG_LEVEL,
        clear_handlers=clear_handlers,
    )

    return log_file


def setup_logging_with_config(
    config_obj,
    mode: str,
    clear_handlers: bool = False,
) -> Path:
    """
    Uses config object to resolve logging directory.
    """
    log_dir = Path(config_obj.logging.log_dir)
    return setup_logging_with_timestamp(log_dir, mode, clear_handlers)


# ============================================================
# 🧠 SECONDARY LOGGER (MOVED HERE FROM LEVEL_4)
# ============================================================

def setup_secondary_log(
    name: str,
    log_file: Path,
    level: str = "INFO",
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    verbose: bool = True,
) -> logging.Logger:
    """
    Creates a secondary logger instance with its own file output.

    This is orchestration logic (NOT handler logic), so it belongs
    in level_3 utilities, not level_4.
    """
    return setup_logger(
        name=name,
        level=level,
        log_file=log_file,
        log_format=log_format,
        verbose=verbose,
        clear_handlers=False,
    )