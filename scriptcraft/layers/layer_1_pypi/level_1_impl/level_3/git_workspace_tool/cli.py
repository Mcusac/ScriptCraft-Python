import argparse

from typing import Sequence

from layers.layer_1_pypi.level_1_impl.level_2.git_workspace_tool.tool import GitWorkspaceTool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="🧰 Git Workspace Tool")
    parser.add_argument(
        "--operation",
        choices=["push", "pull", "status", "commit", "tag"],
        default="push",
        help="Operation to run (default: push)",
    )
    parser.add_argument(
        "--message",
        help="Commit message (used with --operation commit)",
    )
    parser.add_argument(
        "--version",
        help="Version for tagging (used with --operation tag)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    tool = GitWorkspaceTool()
    ok = tool.run(operation=args.operation, message=args.message, version=args.version)
    raise SystemExit(0 if ok else 1)

