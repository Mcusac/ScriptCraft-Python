"""Auto-generated package exports."""


from .compare import compare_datasets

from .datasets import load_datasets_as_list

from .inputs import resolve_input_files

from .logging_setup import (
    resolve_log_dir,
    setup_file_logging,
)

from .plugins import (
    MODE_REGISTRY,
    get_mode,
)

from .reporting import generate_report

__all__ = [
    "MODE_REGISTRY",
    "compare_datasets",
    "generate_report",
    "get_mode",
    "load_datasets_as_list",
    "resolve_input_files",
    "resolve_log_dir",
    "setup_file_logging",
]
