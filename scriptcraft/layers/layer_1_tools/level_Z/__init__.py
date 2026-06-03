"""Auto-generated mixed exports."""


from . import asset_management_orchestrator

from .asset_management_orchestrator import *

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

from .word_2_md import (
    INPUT_FILE,
    convert,
    find_pandoc,
)

__all__ = (
    list(asset_management_orchestrator.__all__)
    + [
        "CustomReleaseManager",
        "INPUT_FILE",
        "check_pip_installation",
        "convert",
        "copy_scriptcraft_tools",
        "create_example_script",
        "example_1_cli_approach",
        "example_2_pipeline_approach",
        "example_3_individual_tools",
        "find_pandoc",
        "install_via_pip",
        "log",
        "logger",
        "setup_git_submodule",
    ]
)
