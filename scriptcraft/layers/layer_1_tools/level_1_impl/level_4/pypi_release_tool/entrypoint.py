"""CLI entrypoint for the PyPI release tool (level_4)."""

import argparse

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_4 import PyPIReleaseTool


def _extend_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--operation",
        choices=["test", "release", "validate", "build"],
        default="test",
        help="Operation to run (default: test)",
    )


def _run_kwargs(args: argparse.Namespace) -> dict:
    return {"operation": args.operation}


main = create_entrypoint_main(
    PyPIReleaseTool,
    tool_name="pypi_release_tool",
    description="PyPI test/release operations for dist artifacts (workspace flows use release_manager pypi mode)",
    parser_kind="tool",
    input_paths_required=False,
    extend_parser_func=_extend_parser,
    run_kwargs_builder=_run_kwargs,
)
