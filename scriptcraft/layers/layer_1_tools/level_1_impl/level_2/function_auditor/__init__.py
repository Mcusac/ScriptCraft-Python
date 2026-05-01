"""Auto-generated package exports."""


from .batch_mode import run_batch_mode

from .cli import build_parser

from .examples import (
    example_batch_audit,
    example_custom_project,
    example_get_unused_functions,
    example_single_file_audit,
)

from .single_file_mode import run_single_file_mode

__all__ = [
    "build_parser",
    "example_batch_audit",
    "example_custom_project",
    "example_get_unused_functions",
    "example_single_file_audit",
    "run_batch_mode",
    "run_single_file_mode",
]
