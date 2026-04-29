"""Dictionary-driven checker core utilities split into cohesive modules."""

from .models import ValidationResult
from .dictionary_validation import validate_against_dictionary
from .runner import run_dictionary_checker

__all__ = [
    "ValidationResult",
    "validate_against_dictionary",
    "run_dictionary_checker",
]

