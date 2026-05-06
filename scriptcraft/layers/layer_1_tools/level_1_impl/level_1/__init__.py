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
    git_submodule_tool,
    git_workspace_tool,
    pypi_release_tool,
    release_manager,
    release_manager_plugins,
    schema_detector,
)

from .automated_labeler import *
from .data_content_comparer import *
from .date_format_standardizer import *
from .dictionary_cleaner import *
from .dictionary_driven_checker import *
from .dictionary_workflow import *
from .function_auditor import *
from .generic_release_tool import *
from .git_submodule_tool import *
from .git_workspace_tool import *
from .pypi_release_tool import *
from .release_manager import *
from .release_manager_plugins import *
from .schema_detector import *

from .compare_columns import compare_columns

from .dictionary_validator_main import DictionaryValidator

from .feature_change_checker_main import FeatureChangeChecker

from .medvisit_integrity_validator_main import (
    FILENAME_MAP,
    MedVisitIntegrityValidator,
)

from .rhq_login_actions import (
    attempt_automatic_login,
    try_click_initial_login_button,
)

from .score_totals_checker_main import ScoreTotalsChecker

from .tool_registry import (
    ToolRegistry,
    dispatch_tool,
    registry,
)

__all__ = (
    list(automated_labeler.__all__)
    + list(data_content_comparer.__all__)
    + list(date_format_standardizer.__all__)
    + list(dictionary_cleaner.__all__)
    + list(dictionary_driven_checker.__all__)
    + list(dictionary_workflow.__all__)
    + list(function_auditor.__all__)
    + list(generic_release_tool.__all__)
    + list(git_submodule_tool.__all__)
    + list(git_workspace_tool.__all__)
    + list(pypi_release_tool.__all__)
    + list(release_manager.__all__)
    + list(release_manager_plugins.__all__)
    + list(schema_detector.__all__)
    + [
        "DictionaryValidator",
        "FILENAME_MAP",
        "FeatureChangeChecker",
        "MedVisitIntegrityValidator",
        "ScoreTotalsChecker",
        "ToolRegistry",
        "attempt_automatic_login",
        "compare_columns",
        "dispatch_tool",
        "registry",
        "try_click_initial_login_button",
    ]
)
