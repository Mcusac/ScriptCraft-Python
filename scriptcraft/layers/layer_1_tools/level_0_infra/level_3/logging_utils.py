import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Union, Dict

from layers.layer_1_tools.level_0_infra.level_1.logger_config import setup_logger
from layers.layer_1_tools.level_0_infra.level_1.paths import LOG_LEVEL

from layers.layer_1_tools.level_0_infra.level_2.logging_bootstrap import build_log_config


# ============================================================
# 🌍 GLOBAL CONFIG (NOW BOOTSTRAPPED CLEANLY)
# ============================================================

config = build_log_config()


# ============================================================
# 🧰 UTILITIES
# ============================================================

def clear_handlers(logger: Optional[logging.Logger] = None) -> None:
    logger = logger or logging.getLogger()
    while logger.handlers:
        logger.removeHandler(logger.handlers[0])


def get_handler_paths() -> Dict[str, Path]:
    logger = logging.getLogger()
    return {
        str(Path(h.baseFilename).resolve()): Path(h.baseFilename)
        for h in logger.handlers
        if isinstance(h, logging.FileHandler)
    }


# ============================================================
# 📝 CORE LOGGING
# ============================================================

def log_message(
    message: str,
    level: str = "info",
    logger_name: str = "root",
    verbose: bool = True,
) -> None:
    setup_logger(message, level=level, logger_name=logger_name, verbose=verbose)


# ============================================================
# 📁 FILE HANDLERS
# ============================================================

def add_file_handler(
    logger_name: str,
    log_file: Union[str, Path],
    level: str = "INFO",
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> None:
    logger = logging.getLogger(logger_name)

    if isinstance(level, str):
        level = getattr(logging, level.upper())

    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(log_file)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(log_format))

    logger.addHandler(handler)
    logger.info(f"Added file handler: {log_file}")


def setup_secondary_log(
    name: str,
    log_file: Union[str, Path],
    level: str = "INFO",
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    verbose: bool = True,
) -> logging.Logger:
    return setup_logger(
        name=name,
        level=level,
        log_file=log_file,
        log_format=log_format,
        verbose=verbose,
        clear_handlers=False,
    )


def setup_logging_with_timestamp(
    log_dir: Path,
    mode: str,
    clear_handlers: bool = False,
) -> Path:
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
    log_dir = Path(config_obj.logging.log_dir)
    return setup_logging_with_timestamp(log_dir, mode, clear_handlers)