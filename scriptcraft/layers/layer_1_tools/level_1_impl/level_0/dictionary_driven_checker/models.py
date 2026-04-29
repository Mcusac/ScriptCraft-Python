
from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationResult:
    """Container for validation results of a single value."""

    row_index: int
    visit_number: int
    column: str
    value: Any
    message: str
    is_warning: bool = False

