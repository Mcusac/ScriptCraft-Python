"""Auto-generated aggregation exports."""


from . import (
    automated_labeler,
    data_content_comparer,
    date_format_standardizer,
    dictionary_cleaner,
    dictionary_driven_checker,
    dictionary_workflow,
    function_auditor,
    pypi_release_tool,
    release_manager,
    rhq_form_autofiller,
    schema_detector,
)

from .automated_labeler import *
from .data_content_comparer import *
from .date_format_standardizer import *
from .dictionary_cleaner import *
from .dictionary_driven_checker import *
from .dictionary_workflow import *
from .function_auditor import *
from .pypi_release_tool import *
from .release_manager import *
from .rhq_form_autofiller import *
from .schema_detector import *

__all__ = (
    list(automated_labeler.__all__)
    + list(data_content_comparer.__all__)
    + list(date_format_standardizer.__all__)
    + list(dictionary_cleaner.__all__)
    + list(dictionary_driven_checker.__all__)
    + list(dictionary_workflow.__all__)
    + list(function_auditor.__all__)
    + list(pypi_release_tool.__all__)
    + list(release_manager.__all__)
    + list(rhq_form_autofiller.__all__)
    + list(schema_detector.__all__)
)
