"""
Centralized CLI utilities for consistent command-line interfaces.
"""

import argparse
import sys

from scriptcraft._version import get_version

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import ensure_tools_discovered
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import StepPipelineEngine
from scriptcraft.layers.layer_1_tools.level_0_infra.level_5 import load_config
from scriptcraft.layers.layer_1_tools.level_0_infra.level_8 import unified_registry
from scriptcraft.layers.layer_1_tools.level_0_infra.level_9 import registry
from scriptcraft.layers.layer_1_tools.level_0_infra.level_10 import (
    InfraRegistryToolLookup,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_11 import (
    dispatch_tool_by_name,
)

def _load_config():
    try:
        return load_config()
    except Exception:
        return None


def main() -> None:
    """Main entry point for ScriptCraft CLI - Industry Standard Interface."""

    parser = argparse.ArgumentParser(
        prog="scriptcraft",
        description="ScriptCraft - Research data processing tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  scriptcraft list
  scriptcraft rhq_form_autofiller
  scriptcraft data_quality
  scriptcraft --help
  scriptcraft --version
""",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"ScriptCraft {get_version()}",
    )

    parser.parse_known_args()

    if len(sys.argv) == 1 or sys.argv[1] in ["--help", "-h", "--version", "list"]:
        handle_list_command()
    else:
        handle_direct_command(sys.argv[1])


def handle_list_command() -> None:
    """Handle the --list command."""

    print("🚀 ScriptCraft - Available Tools and Pipelines")
    print("=" * 50)

    ensure_tools_discovered(unified_registry)

    print("\n📋 Available Tools:")

    for tool_name, description in registry.list_tools().items():
        print(f"  🔧 {tool_name}: {description}")

    config = _load_config()
    if config is not None and config.pipelines:
        print("\n🔷 Available Pipelines:")
        for pipeline_name, pipeline_config in config.pipelines.items():
            description = pipeline_config.get("description", "No description")
            print(f"  🔷 {pipeline_name}: {description}")
    else:
        print("\n⚠️  Pipeline information not available (config not loaded)")

    print("\n💡 Usage Examples:")
    print("  scriptcraft rhq_form_autofiller")
    print("  scriptcraft data_quality")
    print("  scriptcraft --help")


def handle_direct_command(command_name: str) -> None:
    """Handle direct command execution (industry standard pattern)."""

    ensure_tools_discovered(unified_registry)
    lookup = InfraRegistryToolLookup()
    tools = registry.list_tools()

    if lookup.get_tool_class(command_name) is not None:
        dispatch_tool_by_name(command_name, lookup=lookup, exit_on_failure=True)
        return

    config = _load_config()
    if config is not None and command_name in config.pipelines:
        log_and_print(f"🚀 Running pipeline: {command_name}")

        pipeline = StepPipelineEngine(config, command_name)
        success = pipeline.run()

        if success:
            log_and_print(
                f"✅ Pipeline '{command_name}' completed successfully"
            )
        else:
            log_and_print(
                f"❌ Pipeline '{command_name}' failed",
                level="error",
            )
            sys.exit(1)

        return

    log_and_print(f"❌ Command '{command_name}' not found", level="error")
    log_and_print("Available commands:", level="info")
    log_and_print("  Tools:", level="info")

    for name in tools.keys():
        log_and_print(f"    - {name}", level="info")

    if config is not None and config.pipelines:
        log_and_print("  Pipelines:", level="info")
        for name in config.pipelines.keys():
            log_and_print(f"    - {name}", level="info")

    log_and_print("", level="info")
    log_and_print(
        "Use 'scriptcraft list' to see all available commands",
        level="info",
    )

    sys.exit(1)
