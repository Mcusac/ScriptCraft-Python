#!/usr/bin/env python3
"""
Development Usage Examples (EXPERIMENTAL)

TODO: Review whether this should be deleted or moved outside the package runtime
into a docs/examples/scripts folder. It is intentionally placed in level_Z to
avoid bloating the stable runtime API surface.
"""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3.release_pipelines.factory import (
    ReleasePipelineFactory,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import PyPIReleaseTool


def example_1_cli_approach() -> None:
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


def example_2_pipeline_approach() -> None:
    """
    RECOMMENDED: Use pipelines for complex workflows.

    Uses the canonical infra pipeline factory.
    """
    log_and_print("🎯 Pipeline Approach (Recommended for complex workflows)")

    log_and_print("Creating Python package release pipeline (dry run)...")
    pipeline = ReleasePipelineFactory.create_python_package_pipeline(dry_run=True)
    log_and_print(f"Pipeline created: {pipeline.name}")
    log_and_print(f"Steps: {[step.name for step in pipeline.steps]}")


def example_3_individual_tools() -> None:
    """
    RECOMMENDED: Use individual tools for specific operations.
    """
    log_and_print("🎯 Individual Tools Approach (For specific operations)")

    log_and_print("Creating PyPI release tool...")
    pypi_tool = PyPIReleaseTool()
    log_and_print(f"Tool created: {pypi_tool.name}")


def main() -> None:
    """Demonstrate all approaches."""
    log_and_print("🚀 ScriptCraft Development Usage Examples (EXPERIMENTAL)")
    log_and_print("=" * 50)

    example_1_cli_approach()
    log_and_print("")

    example_2_pipeline_approach()
    log_and_print("")

    example_3_individual_tools()
    log_and_print("")


if __name__ == "__main__":
    main()

