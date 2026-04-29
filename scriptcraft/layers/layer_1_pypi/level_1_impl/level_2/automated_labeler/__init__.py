"""Level 1 automated labeler tool entrypoint + public API."""

from .entrypoint import main
from .tool import AutomatedLabeler

__all__ = [
    "AutomatedLabeler",
    "main",
]

