"""Auto-generated mixed exports."""


from . import (
    automated_labeler,
    dictionary_cleaner,
    function_auditor,
    generic_release_tool,
    git_submodule_tool,
    git_workspace_tool,
    release_manager,
)

from .automated_labeler import *
from .dictionary_cleaner import *
from .function_auditor import *
from .generic_release_tool import *
from .git_submodule_tool import *
from .git_workspace_tool import *
from .release_manager import *

from .dictionary_validator_main import DictionaryValidator

from .feature_change_checker_main import FeatureChangeChecker

from .medvisit_integrity_validator_main import (
    FILENAME_MAP,
    MedVisitIntegrityValidator,
)

from .rhq_form_autofiller_main import (
    RHQFormAutofiller,
    attempt_automatic_login,
    load_credentials,
)

from .schema_detector_main import SchemaDetectorTool

from .score_totals_checker_main import ScoreTotalsChecker

__all__ = (
    list(automated_labeler.__all__)
    + list(dictionary_cleaner.__all__)
    + list(function_auditor.__all__)
    + list(generic_release_tool.__all__)
    + list(git_submodule_tool.__all__)
    + list(git_workspace_tool.__all__)
    + list(release_manager.__all__)
    + [
        "DictionaryValidator",
        "FILENAME_MAP",
        "FeatureChangeChecker",
        "MedVisitIntegrityValidator",
        "RHQFormAutofiller",
        "SchemaDetectorTool",
        "ScoreTotalsChecker",
        "attempt_automatic_login",
        "load_credentials",
    ]
)
