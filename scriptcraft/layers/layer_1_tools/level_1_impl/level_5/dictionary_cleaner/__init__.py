"""Level 1 dictionary cleaner tool entrypoint + public API."""

from .entrypoint import main
from .tool import DictionaryCleaner

__all__ = [
    "DictionaryCleaner",
    "main",
]
