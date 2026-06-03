"""CLI entrypoint for schema detector (level_4)."""

import argparse

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import SchemaDetectorTool


def _extend_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--files", nargs="+")
    parser.add_argument("--output", default="output")
    parser.add_argument(
        "--database",
        choices=["sqlite", "sqlserver", "postgresql"],
        default="sqlite",
    )
    parser.add_argument("--sample-size", type=int, default=1000)
    parser.add_argument("--naming", default="pascal_case")
    parser.add_argument("--formats", nargs="+", default=["sql", "json", "yaml"])


def _pre_run(tool: SchemaDetectorTool, args: argparse.Namespace):
    if not args.files:
        return None
    success = tool.run_standalone(
        input_files=args.files,
        output_dir=args.output,
        target_database=args.database,
        sample_size=args.sample_size,
        naming_convention=args.naming,
        output_formats=args.formats,
    )
    return 0 if success else 1


def _run_kwargs(args: argparse.Namespace) -> dict:
    return {
        "input_paths": args.input_paths,
        "output_dir": args.output_dir,
        "domain": args.domain,
        "output_filename": args.output_filename,
        "mode": args.mode,
        "target_database": args.database,
        "privacy_mode": True,
        "sample_size": args.sample_size,
        "naming_convention": args.naming,
        "output_formats": args.formats,
    }


main = create_entrypoint_main(
    SchemaDetectorTool,
    tool_name="schema_detector",
    description="Analyzes datasets and generates database schemas",
    parser_kind="standard",
    input_paths_required=False,
    extend_parser_func=_extend_parser,
    pre_run=_pre_run,
    run_kwargs_builder=_run_kwargs,
)
