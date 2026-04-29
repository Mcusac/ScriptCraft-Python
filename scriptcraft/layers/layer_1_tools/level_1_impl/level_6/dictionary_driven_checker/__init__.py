"""Level 1 dictionary-driven checker tool entrypoint + public API."""

from .entrypoint import main
from .tool import DictionaryDrivenChecker

__all__ = [
    "DictionaryDrivenChecker",
    "main",
]

