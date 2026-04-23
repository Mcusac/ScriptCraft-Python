"""
Centralized test configuration for ScriptCraft.

This module provides consistent path resolution and configuration
for all tests across the workspace, eliminating DRY violations.
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Centralized path resolution
WORKSPACE_ROOT = Path(__file__).parent.parent
PACKAGE_ROOT = WORKSPACE_ROOT / "implementations" / "python-package"
PACKAGE_SCRIPTCRAFT = PACKAGE_ROOT / "scriptcraft"

# Ensure package is in Python path
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

class TestConfig:
    """Centralized test configuration."""
    
    # Paths
    WORKSPACE_ROOT = WORKSPACE_ROOT
    PACKAGE_ROOT = PACKAGE_ROOT
    PACKAGE_SCRIPTCRAFT = PACKAGE_SCRIPTCRAFT
    TESTS_ROOT = WORKSPACE_ROOT / "tests"
    
    # Test categories
    TEST_CATEGORIES = {
        'unit': TESTS_ROOT / "unit",
        'integration': TESTS_ROOT / "integration", 
        'performance': TESTS_ROOT / "performance",
        'tools': TESTS_ROOT / "tools",
        'package': PACKAGE_ROOT / "tests"  # Package-specific tests
    }
    
    # Test runners
    TEST_RUNNERS = {
        'simple': TESTS_ROOT / "run_tests.py",
        'comprehensive': TESTS_ROOT / "run_comprehensive_tests.py",
        'smoke': TESTS_ROOT / "smoke_test.py",
        'package_validation': PACKAGE_ROOT / "validate_before_upload.py"
    }
    
    @classmethod
    def get_package_path(cls) -> Path:
        """Get the package path for imports."""
        return cls.PACKAGE_ROOT
    
    @classmethod
    def get_workspace_path(cls) -> Path:
        """Get the workspace root path."""
        return cls.WORKSPACE_ROOT
    
    @classmethod
    def get_test_category_path(cls, category: str) -> Path:
        """Get path for a specific test category."""
        return cls.TEST_CATEGORIES.get(category, cls.TESTS_ROOT)
    
    @classmethod
    def setup_python_path(cls) -> None:
        """Setup Python path for testing."""
        if str(cls.PACKAGE_ROOT) not in sys.path:
            sys.path.insert(0, str(cls.PACKAGE_ROOT))
    
    @classmethod
    def get_test_config(cls) -> Dict[str, Any]:
        """Get complete test configuration."""
        return {
            'workspace_root': str(cls.WORKSPACE_ROOT),
            'package_root': str(cls.PACKAGE_ROOT),
            'package_scriptcraft': str(cls.PACKAGE_SCRIPTCRAFT),
            'tests_root': str(cls.TESTS_ROOT),
            'test_categories': {k: str(v) for k, v in cls.TEST_CATEGORIES.items()},
            'test_runners': {k: str(v) for k, v in cls.TEST_RUNNERS.items()}
        }

# Auto-setup Python path when module is imported
TestConfig.setup_python_path()
