"""Auto-generated mixed exports."""


from . import (
    automated_labeler,
    data_content_comparer,
    date_format_standardizer,
    dictionary_cleaner,
    dictionary_driven_checker,
    dictionary_workflow,
    function_auditor,
    generic_release_tool,
    git,
    release_manager,
    release_manager_plugins,
)

from .automated_labeler import *
from .data_content_comparer import *
from .date_format_standardizer import *
from .dictionary_cleaner import *
from .dictionary_driven_checker import *
from .dictionary_workflow import *
from .function_auditor import *
from .generic_release_tool import *
from .git import *
from .release_manager import *
from .release_manager_plugins import *

from .compare_columns import compare_columns

from .dictionary_driven_checker_env import setup_environment

from .rhq_login_actions import (
    attempt_automatic_login,
    try_click_initial_login_button,
)

from .runtime_normalize import normalize_list

from .sys_path import (
    ensure_sys_path,
    setup_import_paths_common,
)

from .tooling_dispatcher import dispatch_tool

__all__ = (
    list(automated_labeler.__all__)
    + list(data_content_comparer.__all__)
    + list(date_format_standardizer.__all__)
    + list(dictionary_cleaner.__all__)
    + list(dictionary_driven_checker.__all__)
    + list(dictionary_workflow.__all__)
    + list(function_auditor.__all__)
    + list(generic_release_tool.__all__)
    + list(git.__all__)
    + list(release_manager.__all__)
    + list(release_manager_plugins.__all__)
    + [
        "attempt_automatic_login",
        "compare_columns",
        "dispatch_tool",
        "ensure_sys_path",
        "normalize_list",
        "setup_environment",
        "setup_import_paths_common",
        "try_click_initial_login_button",
    ]
)
