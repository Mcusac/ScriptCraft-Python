"""DRY CLI entrypoint factory for tool ``main()`` functions."""

import argparse
import sys

from collections.abc import Callable
from typing import Any, Optional, Type

from scriptcraft.layers.layer_0_core.level_0 import (
    filter_kwargs_for_callable,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    ParserKind,
    RunStyle,
    TTool,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import setup_logger
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import ParserFactory


def create_entrypoint_main(
    tool_class: Type[TTool],
    *,
    tool_name: str,
    description: str,
    parser_kind: ParserKind = "standard",
    run_style: RunStyle = "kwargs",
    input_paths_required: bool = True,
    create_parser_func: Optional[Callable[[], argparse.ArgumentParser]] = None,
    extend_parser_func: Optional[Callable[[argparse.ArgumentParser], None]] = None,
    run_kwargs_builder: Optional[Callable[[argparse.Namespace], dict[str, Any]]] = None,
    pre_run: Optional[Callable[[Any, argparse.Namespace], Optional[int]]] = None,
    exit_on_error: bool = True,
) -> Callable[[], None]:
    """Create a DRY ``main()`` for tool entrypoints."""

    def _create_parser() -> argparse.ArgumentParser:
        if parser_kind == "custom":
            if not create_parser_func:
                raise ValueError("create_parser_func is required when parser_kind='custom'")
            return create_parser_func()

        if parser_kind == "dictionary_workflow":
            return ParserFactory.create_dictionary_workflow_parser(tool_name, description)

        if parser_kind == "tool":
            return ParserFactory.create_tool_parser(tool_name, description)

        if parser_kind == "standard":
            parser = ParserFactory.create_standard_tool_parser(
                tool_name,
                description,
                input_paths_required=input_paths_required,
            )
            if extend_parser_func:
                extend_parser_func(parser)
            return parser

        raise ValueError(f"Unknown parser_kind: {parser_kind}")

    def _build_run_kwargs(args: argparse.Namespace) -> dict[str, Any]:
        if run_kwargs_builder:
            return run_kwargs_builder(args)
        return dict(vars(args))

    def main() -> None:
        try:
            parser = _create_parser()
            args = parser.parse_args()

            tool = tool_class()  # type: ignore[call-arg]

            if pre_run is not None:
                early_exit = pre_run(tool, args)
                if early_exit is not None:
                    if exit_on_error:
                        sys.exit(early_exit)
                    return

            if run_style == "namespace":
                run_func = getattr(tool, "run")
                run_func(args)  # type: ignore[misc]
                return

            tool_kwargs = _build_run_kwargs(args)
            run_func = getattr(tool, "run")
            tool_kwargs = filter_kwargs_for_callable(run_func, tool_kwargs)
            run_func(**tool_kwargs)  # type: ignore[misc]

        except KeyboardInterrupt:
            setup_logger("🛑 Interrupted by user", level="error")
            if exit_on_error:
                sys.exit(1)
            return
        except SystemExit:
            raise
        except Exception as e:
            setup_logger(f"❌ Fatal error in {tool_name}: {e}", level="error")
            if exit_on_error:
                sys.exit(1)
            return

    return main
