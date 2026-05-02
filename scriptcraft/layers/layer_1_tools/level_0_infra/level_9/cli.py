"""
Centralized CLI utilities for consistent command-line interfaces.
"""

import argparse
import sys

from layers.layer_1_tools.level_0_infra.level_0.version import get_version
from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_2.root_schema import Config
from layers.layer_1_tools.level_0_infra.level_2.pipeline_base import BasePipeline
from layers.layer_1_tools.level_0_infra.level_8.registry import unified_registry


# ============================================================
# ENTRYPOINT
# ============================================================

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
"""
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"ScriptCraft {get_version()}"
    )

    parser.parse_known_args()

    if len(sys.argv) == 1 or sys.argv[1] in ["--help", "-h", "--version", "list"]:
        handle_list_command()
    else:
        handle_direct_command(sys.argv[1])


# ============================================================
# LIST COMMAND
# ============================================================

def handle_list_command() -> None:
    """Handle the --list command."""

    print("🚀 ScriptCraft - Available Tools and Pipelines")
    print("=" * 50)

    unified_registry.discover_tools()

    print("\n📋 Available Tools:")

    tools = unified_registry.get_available_tools()

    for tool_name, tool_class in tools.items():
        description = getattr(tool_class, "description", "No description")
        print(f"  🔧 {tool_name}: {description}")

    # Pipelines (unchanged behavior)
    try:
        config = Config()

        if hasattr(config, "pipelines") and config.pipelines:
            print("\n🔷 Available Pipelines:")

            for pipeline_name, pipeline_config in config.pipelines.items():
                description = pipeline_config.get("description", "No description")
                print(f"  🔷 {pipeline_name}: {description}")

    except Exception:
        print("\n⚠️  Pipeline information not available (config not loaded)")

    print("\n💡 Usage Examples:")
    print("  scriptcraft rhq_form_autofiller")
    print("  scriptcraft data_quality")
    print("  scriptcraft --help")


# ============================================================
# DIRECT COMMAND EXECUTION
# ============================================================

def handle_direct_command(command_name: str) -> None:
    """Handle direct command execution (industry standard pattern)."""

    unified_registry.discover_tools()

    # ================================
    # TOOL EXECUTION PATH
    # ================================

    tool_cls = unified_registry.get_tool(command_name, create_instance=False)

    tools = unified_registry.get_available_tools()

    if tool_cls:
        log_and_print(f"🚀 Running tool: {command_name}")

        try:
            tool_instance = tool_cls()

            success = tool_instance.run()

            if success:
                log_and_print(f"✅ Tool '{command_name}' completed successfully")
            else:
                log_and_print(f"❌ Tool '{command_name}' failed", level="error")
                sys.exit(1)

        except Exception as e:
            log_and_print(
                f"❌ Error running tool '{command_name}': {e}",
                level="error"
            )
            sys.exit(1)

        return

    # ================================
    # PIPELINE EXECUTION PATH
    # ================================

    try:
        config = Config()

        if hasattr(config, "pipelines") and command_name in config.pipelines:
            log_and_print(f"🚀 Running pipeline: {command_name}")

            pipeline = BasePipeline(config, command_name)
            success = pipeline.run()

            if success:
                log_and_print(
                    f"✅ Pipeline '{command_name}' completed successfully"
                )
            else:
                log_and_print(
                    f"❌ Pipeline '{command_name}' failed",
                    level="error"
                )
                sys.exit(1)

            return

    except Exception:
        pass

    # ================================
    # ERROR PATH (UNCHANGED LOGIC)
    # ================================

    log_and_print(f"❌ Command '{command_name}' not found", level="error")

    log_and_print("Available commands:", level="info")
    log_and_print("  Tools:", level="info")

    for name in tools.keys():
        log_and_print(f"    - {name}", level="info")

    try:
        config = Config()

        if hasattr(config, "pipelines"):
            log_and_print("  Pipelines:", level="info")

            for name in config.pipelines.keys():
                log_and_print(f"    - {name}", level="info")

    except Exception:
        pass

    log_and_print("", level="info")
    log_and_print(
        "Use 'scriptcraft list' to see all available commands",
        level="info"
    )

    sys.exit(1)