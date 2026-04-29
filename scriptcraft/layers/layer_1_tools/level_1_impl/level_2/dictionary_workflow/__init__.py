"""Level 1 dictionary workflow tool entrypoint + public API."""

from .entrypoint import main
from .tool import DictionaryWorkflow

__all__ = [
    "DictionaryWorkflow",
    "main",
]

