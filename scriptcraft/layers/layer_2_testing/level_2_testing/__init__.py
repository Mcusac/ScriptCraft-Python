"""Auto-generated mixed exports."""


from . import (
    integration,
    performance,
)

from .integration import *
from .performance import *

from .conftest import (
    PACKAGE_PATH,
    package_path,
    sample_comparison_files,
    sample_docx_template,
    sample_excel_file,
    sample_paths,
    scriptcraft_import,
    temp_dir,
    temp_output_dir,
    test_data_dir,
)

from .run_comprehensive_tests import (
    TestRunner,
    project_root,
)

from .smoke_test import (
    project_root,
    test_base_functionality,
    test_imports,
    test_tool_imports,
)

from .unified_test_runner import UnifiedTestRunner

from .validate_before_upload import (
    run_command,
    validate_package,
)

__all__ = (
    list(integration.__all__)
    + list(performance.__all__)
    + [
        "PACKAGE_PATH",
        "TestRunner",
        "UnifiedTestRunner",
        "package_path",
        "project_root",
        "run_command",
        "sample_comparison_files",
        "sample_docx_template",
        "sample_excel_file",
        "sample_paths",
        "scriptcraft_import",
        "temp_dir",
        "temp_output_dir",
        "test_base_functionality",
        "test_data_dir",
        "test_imports",
        "test_tool_imports",
        "validate_package",
    ]
)
