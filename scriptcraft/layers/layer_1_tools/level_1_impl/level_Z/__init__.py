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
    example_4_run_all_approach,
    example_5_anti_pattern,
)

from .git_pipelines import (
    GitPipelineFactory,
    create_full_git_sync_pipeline,
    create_pypi_release_pipeline,
    create_pypi_test_pipeline,
    create_submodule_sync_pipeline,
    create_workspace_push_pipeline,
)

from .pipeline_utils import (
    add_supplement_steps,
    list_pipelines,
    make_step,
    preview_pipeline,
    run_global_tool,
    run_pipeline,
    run_pipeline_from_steps,
    run_qc_for_each_domain,
    run_qc_for_single_domain,
    run_qc_single_step,
    timed_pipeline,
    validate_pipelines,
)

from .release_cli import (
    full_release,
    git_status,
    git_sync,
    pypi_release,
    pypi_test,
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
        "GitPipelineFactory",
        "add_supplement_steps",
        "check_pip_installation",
        "copy_scriptcraft_tools",
        "create_example_script",
        "create_full_git_sync_pipeline",
        "create_pypi_release_pipeline",
        "create_pypi_test_pipeline",
        "create_submodule_sync_pipeline",
        "create_workspace_push_pipeline",
        "example_1_cli_approach",
        "example_2_pipeline_approach",
        "example_3_individual_tools",
        "example_4_run_all_approach",
        "example_5_anti_pattern",
        "full_release",
        "git_status",
        "git_sync",
        "install_via_pip",
        "list_pipelines",
        "log",
        "logger",
        "make_step",
        "preview_pipeline",
        "pypi_release",
        "pypi_test",
        "run_global_tool",
        "run_pipeline",
        "run_pipeline_from_steps",
        "run_qc_for_each_domain",
        "run_qc_for_single_domain",
        "run_qc_single_step",
        "setup_git_submodule",
        "timed_pipeline",
        "validate_pipelines",
    ]
)
