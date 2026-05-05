"""Auto-generated mixed exports."""


from . import (
    dictionary_cleaner,
    function_auditor,
)

from .dictionary_cleaner import *
from .function_auditor import *

from .development_usage import (
    example_1_cli_approach,
    example_2_pipeline_approach,
    example_3_individual_tools,
    example_4_run_all_approach,
    example_5_anti_pattern,
)

from .release_cli import (
    full_release,
    git_status,
    git_sync,
    pypi_release,
    pypi_test,
)

__all__ = (
    list(dictionary_cleaner.__all__)
    + list(function_auditor.__all__)
    + [
        "example_1_cli_approach",
        "example_2_pipeline_approach",
        "example_3_individual_tools",
        "example_4_run_all_approach",
        "example_5_anti_pattern",
        "full_release",
        "git_status",
        "git_sync",
        "pypi_release",
        "pypi_test",
    ]
)
