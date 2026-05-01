"""Auto-generated mixed exports."""


from . import (
    automated_labeler,
    data_content_comparer,
    dictionary_cleaner,
    dictionary_workflow,
    function_auditor,
    generic_release_tool,
    git_submodule_tool,
    git_workspace_tool,
    release_manager,
)

from .automated_labeler import *
from .data_content_comparer import *
from .dictionary_cleaner import *
from .dictionary_workflow import *
from .function_auditor import *
from .generic_release_tool import *
from .git_submodule_tool import *
from .git_workspace_tool import *
from .release_manager import *

from .rhq_flow import (
    handle_login,
    submit_form,
)

from .rhq_form_autofiller_env import setup_environment

from .runtime_loops import (
    run_domains,
    run_process_domain_for_single_pair,
    run_process_domain_over_input_paths,
)

from .setup_basic_tool_environment import setup_basic_tool_environment

from .tool_registry import (
    ToolRegistry,
    dispatch_tool,
    registry,
)

__all__ = (
    list(automated_labeler.__all__)
    + list(data_content_comparer.__all__)
    + list(dictionary_cleaner.__all__)
    + list(dictionary_workflow.__all__)
    + list(function_auditor.__all__)
    + list(generic_release_tool.__all__)
    + list(git_submodule_tool.__all__)
    + list(git_workspace_tool.__all__)
    + list(release_manager.__all__)
    + [
        "ToolRegistry",
        "dispatch_tool",
        "handle_login",
        "registry",
        "run_domains",
        "run_process_domain_for_single_pair",
        "run_process_domain_over_input_paths",
        "setup_basic_tool_environment",
        "setup_environment",
        "submit_form",
    ]
)
