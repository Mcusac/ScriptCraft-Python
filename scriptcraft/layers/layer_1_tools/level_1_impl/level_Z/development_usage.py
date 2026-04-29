#!/usr/bin/env python3
"""
Development Usage Examples

This file demonstrates the recommended approaches for using ScriptCraft
in development, following industry standards and DRY principles.
"""

import sys

from pathlib import Path

# Add the package to path (only needed for development)
sys.path.insert(0, str(Path(__file__).parent.parent / "implementations" / "python-package"))

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_pypi.level_0_infra.level_Z.git_pipelines import (
    create_pypi_test_pipeline,
)

from layers.layer_1_pypi.tools.pypi_release_tool.main import PyPIReleaseTool

def example_1_cli_approach():
    """
    RECOMMENDED: Use CLI commands for simple operations.
    
    In terminal:
    scriptcraft-release pypi-test
    scriptcraft-release pypi-release
    scriptcraft-release git-sync
    """
    log_and_print("🎯 CLI Approach (Recommended for simple operations)")
    log_and_print("Run these commands in terminal:")
    log_and_print("  scriptcraft-release pypi-test")
    log_and_print("  scriptcraft-release pypi-release")
    log_and_print("  scriptcraft-release git-sync")
    log_and_print("  scriptcraft-release full-release")
    log_and_print("  scriptcraft --tool rhq_form_autofiller")
    log_and_print("  scriptcraft --tool data_content_comparer")

def example_2_pipeline_approach():
    """
    RECOMMENDED: Use pipelines for complex workflows.
    
    This approach uses the consolidated pipeline system and
    follows ScriptCraft patterns.
    """
    log_and_print("🎯 Pipeline Approach (Recommended for complex workflows)")
    
    # Create and run PyPI test pipeline
    log_and_print("Creating PyPI test pipeline...")
    pipeline = create_pypi_test_pipeline()
    log_and_print(f"Pipeline created: {pipeline.name}")
    log_and_print(f"Steps: {[step.name for step in pipeline.steps]}")
    
    # You can run it with: pipeline.run()
    # log_and_print("Running pipeline...")
    # pipeline.run()

def example_3_individual_tools():
    """
    RECOMMENDED: Use individual tools for specific operations.
    
    This approach gives you fine-grained control while still
    using the ScriptCraft tool system.
    """
    log_and_print("🎯 Individual Tools Approach (For specific operations)")
    
    # Create and run individual tools
    log_and_print("Creating PyPI release tool...")
    pypi_tool = PyPIReleaseTool()
    log_and_print(f"Tool created: {pypi_tool.name}")
    
    # You can run specific operations
    # pypi_tool.run(operation="test")
    # pypi_tool.run(operation="build")
    # pypi_tool.run(operation="release")

def example_4_run_all_approach():
    """
    RECOMMENDED: Use run_all.py for complex orchestration.
    
    This mimics your distributable pattern and uses config.yaml
    as the single source of truth.
    """
    log_and_print("🎯 run_all.py Approach (For complex orchestration)")
    log_and_print("Run these commands in terminal:")
    log_and_print("  python run_all.py --list")
    log_and_print("  python run_all.py --pipeline data_quality")
    log_and_print("  python run_all.py --pipeline dictionary_pipeline")
    log_and_print("  python run_all.py --tool rhq_form_autofiller")
    log_and_print("  python run_all.py --tool data_content_comparer")

def example_5_anti_pattern():
    """
    ANTI-PATTERN: Don't create simple scripts for everything.
    
    This breaks DRY principles and doesn't use the config system.
    """
    log_and_print("❌ Anti-Pattern: Simple Scripts (Avoid)")
    log_and_print("Don't create scripts like this:")
    log_and_print("  # my_custom_script.py")
    log_and_print("  # Hardcoded logic that duplicates functionality")
    log_and_print("  # Not config-driven")
    log_and_print("  # Not distributable")
    log_and_print("  # Breaks DRY principles")

def main():
    """Demonstrate all approaches."""
    log_and_print("🚀 ScriptCraft Development Usage Examples")
    log_and_print("=" * 50)
    
    example_1_cli_approach()
    log_and_print("")
    
    example_2_pipeline_approach()
    log_and_print("")
    
    example_3_individual_tools()
    log_and_print("")
    
    example_4_run_all_approach()
    log_and_print("")
    
    example_5_anti_pattern()
    log_and_print("")
    
    log_and_print("🎯 RECOMMENDATION:")
    log_and_print("1. Use CLI commands for simple operations")
    log_and_print("2. Use run_all.py for complex workflows")
    log_and_print("3. Use pipelines for multi-step processes")
    log_and_print("4. Use individual tools for specific operations")
    log_and_print("5. Avoid simple scripts (anti-DRY)")

if __name__ == "__main__":
    main()
