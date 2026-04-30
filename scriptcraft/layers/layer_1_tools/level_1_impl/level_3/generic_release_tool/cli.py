"""
CLI for the Generic Release Tool.
"""

import argparse

from layers.layer_1_tools.level_1_impl.level_2.generic_release_tool.tool import GenericReleaseTool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="🚀 Generic Release Tool")
    parser.add_argument(
        "--pipeline",
        choices=["python_package", "git_repo", "docs", "full"],
        default="python_package",
        help="Release pipeline to run",
    )
    parser.add_argument("--version", help="Version to release")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    tool = GenericReleaseTool()
    tool.run(
        pipeline=args.pipeline,
        version=args.version,
        dry_run=args.dry_run,
    )

