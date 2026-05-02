"""
Logging handlers facade.

This module intentionally contains only lightweight stdlib wrappers.
No orchestration logic or cross-layer dependencies should live here.
"""

import logging
from pathlib import Path
from typing import Optional, Union


# ============================================================
# 📁 STDLIB WRAPPERS (ONLY SAFE TO REMOVE ANY TIME)
# ============================================================

def create_file_handler(
    log_file: Union[str, Path],
    level: int = logging.INFO,
    formatter: Optional[logging.Formatter] = None,
) -> logging.FileHandler:
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)

    if formatter:
        handler.setFormatter(formatter)

    return handler


def create_console_handler(
    level: int = logging.INFO,
    formatter: Optional[logging.Formatter] = None,
) -> logging.StreamHandler:
    handler = logging.StreamHandler()
    handler.setLevel(level)

    if formatter:
        handler.setFormatter(formatter)

    return handler