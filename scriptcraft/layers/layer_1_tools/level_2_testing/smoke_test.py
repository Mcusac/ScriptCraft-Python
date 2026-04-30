#!/usr/bin/env python3
"""
Smoke Test for ScriptCraft

Quick verification that all tools can be imported and instantiated.
This is a fast test to ensure the basic functionality works.
"""

import sys
from pathlib import Path
import traceback

# Use centralized test configuration
from test_config import TestConfig
project_root = TestConfig.WORKSPACE_ROOT

# Ensure we can print unicode (Windows console defaults can be cp1252).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def test_imports():
    """Test that all core modules can be imported."""
    print("🔍 Testing core imports...")
    
    import_tests = [
        ('scriptcraft', 'Main package'),
        ('scriptcraft.layers', 'Layered namespace'),
        ('layers.layer_1_pypi.level_0_infra.level_0.logging_core', 'Infra logging core'),
        ('layers.layer_1_pypi.level_0_infra.level_7.registry', 'Unified registry'),
        ('layers.layer_1_pypi.level_1_impl', 'Implementation layer'),
    ]
    
    failed_imports = []
    
    for module_name, description in import_tests:
        try:
            __import__(module_name)
            print(f"  ✅ {description}")
        except Exception as e:
            print(f"  ❌ {description}: {e}")
            failed_imports.append((module_name, str(e)))
    
    return failed_imports


def test_tool_imports():
    """Test that all tools can be imported and instantiated."""
    print("\n🔧 Testing tool imports...")
    
    try:
        from layers.layer_1_tools.level_1_impl import get_available_tools
        tools = get_available_tools()
    except Exception as e:
        print(f"  ❌ Failed to get available tools: {e}")
        return []
    
    failed_tools = []
    
    for tool_name, tool_class in tools.items():
        try:
            if tool_class is not None:
                print(f"  ✅ {tool_name}")
            else:
                print(f"  ⚠️ {tool_name}: Tool class is None")
                failed_tools.append((tool_name, "Tool class is None"))
        except Exception as e:
            print(f"  ❌ {tool_name}: {e}")
            failed_tools.append((tool_name, str(e)))
    
    return failed_tools


def test_base_functionality():
    """Test basic functionality like config loading and logging."""
    print("\n⚙️ Testing base functionality...")
    
    failed_tests = []
    
    # Test logging core import + call
    try:
        from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print

        log_and_print("✅ Logging core import OK")
        print("  ✅ Logging core")
    except Exception as e:
        print(f"  ❌ Logging core: {e}")
        failed_tests.append(("logging_core", str(e)))
    
    return failed_tests


def main():
    """Run all smoke tests."""
    print("🚀 ScriptCraft Smoke Test")
    print("=" * 40)
    
    # Test imports
    failed_imports = test_imports()
    
    # Test tool imports
    failed_tools = test_tool_imports()
    
    # Test base functionality
    failed_functionality = test_base_functionality()
    
    # Summary
    print("\n📊 SUMMARY")
    print("=" * 40)
    
    total_failures = len(failed_imports) + len(failed_tools) + len(failed_functionality)
    
    if total_failures == 0:
        print("🎉 ALL SMOKE TESTS PASSED!")
        print("ScriptCraft is ready for comprehensive testing.")
        return True
    else:
        print(f"❌ {total_failures} smoke tests failed:")
        
        if failed_imports:
            print(f"  - {len(failed_imports)} import failures")
            for module, error in failed_imports:
                print(f"    {module}: {error}")
        
        if failed_tools:
            print(f"  - {len(failed_tools)} tool failures")
            for tool, error in failed_tools:
                print(f"    {tool}: {error}")
        
        if failed_functionality:
            print(f"  - {len(failed_functionality)} functionality failures")
            for test, error in failed_functionality:
                print(f"    {test}: {error}")
        
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 