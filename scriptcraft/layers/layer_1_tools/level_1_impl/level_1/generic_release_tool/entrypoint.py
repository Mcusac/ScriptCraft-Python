"""CLI entrypoint for the generic release tool (level_1)."""

import argparse

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import GenericReleaseTool


def _extend_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--pipeline",
        choices=["python_package", "git_repo", "docs", "full"],
        default="python_package",
        help="Release pipeline to run (standalone repos only; workspace releases use release_manager)",
    )
    parser.add_argument("--version", help="Version to release")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")


def _run_kwargs(args: argparse.Namespace) -> dict:
    return {
        "pipeline": args.pipeline,
        "version": args.version,
        "dry_run": args.dry_run,
    }


main = create_entrypoint_main(
    GenericReleaseTool,
    tool_name="generic_release_tool",
    description="Generic release tool for standalone repos (not workspace-integrated release_manager flows)",
    parser_kind="tool",
    input_paths_required=False,
    extend_parser_func=_extend_parser,
    run_kwargs_builder=_run_kwargs,
)
