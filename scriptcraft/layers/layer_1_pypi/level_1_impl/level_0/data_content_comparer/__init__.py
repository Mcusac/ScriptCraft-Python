"""Data content comparer domain utilities (cohesive, DRY modules)."""

from .plugins import load_mode
from .inputs import resolve_input_files
from .datasets import load_datasets_as_list
from .compare import compare_datasets
from .reporting import generate_report

__all__ = [
    "load_mode",
    "resolve_input_files",
    "load_datasets_as_list",
    "compare_datasets",
    "generate_report",
]

