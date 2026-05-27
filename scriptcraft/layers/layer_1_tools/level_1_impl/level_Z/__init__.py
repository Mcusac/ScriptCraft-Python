"""Auto-generated mixed exports."""


from . import dictionary_driven_checker_plugins

from .dictionary_driven_checker_plugins import *

from .custom_release_script import (
    CustomReleaseManager,
    logger,
)

from .development_usage import (
    example_1_cli_approach,
    example_2_pipeline_approach,
    example_3_individual_tools,
)

from .setup_scriptcraft_in_project import (
    check_pip_installation,
    copy_scriptcraft_tools,
    create_example_script,
    install_via_pip,
    log,
    setup_git_submodule,
)

__all__ = (
    list(dictionary_driven_checker_plugins.__all__)
    + [
        "CustomReleaseManager",
        "check_pip_installation",
        "copy_scriptcraft_tools",
        "create_example_script",
        "example_1_cli_approach",
        "example_2_pipeline_approach",
        "example_3_individual_tools",
        "install_via_pip",
        "log",
        "logger",
        "setup_git_submodule",
    ]
)
