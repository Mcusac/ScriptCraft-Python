#!/usr/bin/env python3
"""
🧪 Import Pattern Tests

Test all documented import patterns to ensure they work correctly.
"""

import sys
from pathlib import Path

# Add the package to the path for testing
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_basic_import():
    """Test basic package import."""
    import scriptcraft
    assert hasattr(scriptcraft, '__version__')
    print(f"✅ Basic import works - version: {scriptcraft.__version__}")

def test_common_import():
    """Test canonical barrel imports for shared utilities."""
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import setup_logger
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import Config
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool

    assert BaseTool is not None
    assert Config is not None
    assert setup_logger is not None
    assert log_and_print is not None
    print("✅ Barrel imports work")

def test_specific_imports():
    """Test specific imports from infra barrels."""
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import setup_logger
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import Config
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool
    assert BaseTool is not None
    assert Config is not None
    assert setup_logger is not None
    assert log_and_print is not None
    print("✅ Specific imports work")

def test_tool_imports():
    """Test tool imports via level barrels."""
    from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
        AutomatedLabeler,
        RHQFormAutofiller,
    )
    from scriptcraft.layers.layer_1_tools.level_1_impl.level_3 import DataContentComparer
    
    # Test instantiation
    labeler = AutomatedLabeler()
    comparer = DataContentComparer()
    autofiller = RHQFormAutofiller()
    
    assert labeler.name == "Automated Labeler"
    assert comparer.name == "Data Content Comparer"
    assert autofiller.name == "RHQ Form Autofiller"
    print("✅ Tool imports work")

def test_tool_discovery():
    """Test tool discovery."""
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
        get_tools_by_category,
    )
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_8 import get_available_tools

    tools = get_available_tools()
    assert len(tools) > 0

    categories = get_tools_by_category()
    assert len(categories) > 0
    
    print(f"✅ Tool discovery works - {len(tools)} tools found")

def test_pipeline_imports():
    """Test pipeline imports."""
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
        PipelineStep,
        StepPipelineEngine,
    )
    assert StepPipelineEngine is not None
    assert PipelineStep is not None
    print("✅ Pipeline imports work")

def test_config_usage():
    """Test configuration usage."""
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import Config
    
    # Test config loading (should work with environment fallback)
    config = Config.from_yaml("nonexistent.yaml")
    assert config is not None
    
    # Test tool config access
    tool_config = config.get_tool_config("test_tool")
    assert tool_config is not None
    print("✅ Config usage works")

def test_logging_usage():
    """Test logging usage."""
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import setup_logger
    
    # Test logging setup
    logger = setup_logger("test_logger")
    assert logger is not None
    
    # Test log and print
    log_and_print("✅ Test message")
    print("✅ Logging usage works")

def run_all_tests():
    """Run all import pattern tests."""
    print("🧪 Testing Import Patterns...")
    print("=" * 40)
    
    tests = [
        test_basic_import,
        test_common_import,
        test_specific_imports,
        test_tool_imports,
        test_tool_discovery,
        test_pipeline_imports,
        test_config_usage,
        test_logging_usage
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            return False
    
    print("\n" + "=" * 40)
    print("✅ All import pattern tests passed!")
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
