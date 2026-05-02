"""
Unified Main Runner for ScriptCraft Tools

This module provides a standardized way to run tools from both development
and distributable environments. It consolidates CLI patterns and eliminates
duplication across tools.

Usage:
    # In __main__.py files:
    from scriptcraft.common.cli.main_runner import run_tool_main

    if __name__ == "__main__":
        run_tool_main("tool_name", "Tool description")
"""

import sys
import argparse

from typing import Optional, Callable, Any, Dict, Type
from abc import ABC, abstractmethod

from layers.layer_1_tools.level_0_infra.level_1.logger_config import setup_logger
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool
from layers.layer_1_tools.level_0_infra.level_6.argument_parsers import ParserFactory


class ToolRunner(ABC):
    """Abstract base class for tool runners."""

    @abstractmethod
    def create_parser(self) -> argparse.ArgumentParser:
        pass

    @abstractmethod
    def run_tool(self, args: argparse.Namespace, **kwargs) -> bool:
        pass


class StandardToolRunner(ToolRunner):
    """Standard tool runner that works with BaseTool subclasses."""

    def __init__(self, tool_class: Type[BaseTool], tool_name: str, description: str) -> None:
        self.tool_class = tool_class
        self.tool_name = tool_name
        self.description = description
        self.logger = setup_logger(tool_name)

    def create_parser(self) -> argparse.ArgumentParser:
        parser = ParserFactory.create_tool_parser(self.tool_name, self.description)

        if hasattr(self.tool_class, "add_cli_arguments"):
            self.tool_class.add_cli_arguments(parser)

        return parser

    def run_tool(self, args: argparse.Namespace, **kwargs) -> bool:
        try:
            tool = self.tool_class(
                name=self.tool_name,
                description=self.description
            )

            tool_kwargs: Dict[str, Any] = vars(args)

            if hasattr(args, "input_paths") and args.input_paths:
                tool_kwargs["input_paths"] = args.input_paths

            tool.run(**tool_kwargs, **kwargs)

            self.logger.info(f"✅ {self.tool_name} completed successfully")
            return True

        except Exception as e:
            self.logger.error(f"❌ {self.tool_name} failed: {e}")
            return False


class CustomToolRunner(ToolRunner):
    """Custom tool runner for tools that need special handling."""

    def __init__(
        self,
        create_parser_func: Callable[[], argparse.ArgumentParser],
        run_func: Callable[[argparse.Namespace], bool],
        tool_name: str = "custom_tool",
    ) -> None:
        self.create_parser_func = create_parser_func
        self.run_func = run_func
        self.logger = setup_logger(tool_name)

    def create_parser(self) -> argparse.ArgumentParser:
        return self.create_parser_func()

    def run_tool(self, args: argparse.Namespace, **kwargs) -> bool:
        try:
            success = self.run_func(args, **kwargs)

            if success:
                self.logger.info("✅ Tool completed successfully")
            else:
                self.logger.error("❌ Tool failed")

            return success

        except Exception as e:
            self.logger.error(f"❌ Tool crashed: {e}")
            return False


def run_tool_main(
    tool_name: str,
    description: str,
    tool_class: Optional[Type[BaseTool]] = None,
    create_parser_func: Optional[Callable[[], argparse.ArgumentParser]] = None,
    run_func: Optional[Callable[[argparse.Namespace], bool]] = None,
    **kwargs,
) -> int:
    """
    Main entry point for tool execution.
    """

    try:
        if tool_class and issubclass(tool_class, BaseTool):
            runner: ToolRunner = StandardToolRunner(tool_class, tool_name, description)
        elif create_parser_func and run_func:
            runner = CustomToolRunner(create_parser_func, run_func, tool_name)
        else:
            raise ValueError(
                "Must provide either tool_class or both create_parser_func and run_func"
            )

        parser = runner.create_parser()
        args = parser.parse_args()

        logger = setup_logger(tool_name)
        logger.info(f"🚀 Starting {tool_name}")

        success = runner.run_tool(args, **kwargs)

        return 0 if success else 1

    except KeyboardInterrupt:
        setup_logger("root").warning("🛑 Tool interrupted by user")
        return 1

    except Exception as e:
        setup_logger("root").error(f"❌ Fatal error: {e}")
        return 1


def run_tool_from_cli(
    tool_name: str,
    description: str,
    tool_class: Optional[Type[BaseTool]] = None,
    **kwargs: Any,
) -> None:
    exit_code = run_tool_main(tool_name, description, tool_class, **kwargs)
    sys.exit(exit_code)


# ===== LEGACY SUPPORT =====

def create_standard_parser(tool_name: str, description: str) -> argparse.ArgumentParser:
    return ParserFactory.create_tool_parser(tool_name, description)


def run_with_standard_args(
    tool_class: Type[BaseTool],
    tool_name: str,
    description: str
) -> int:
    return run_tool_main(tool_name, description, tool_class=tool_class)