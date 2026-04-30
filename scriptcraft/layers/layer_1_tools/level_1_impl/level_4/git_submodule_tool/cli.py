
import argparse
from typing import Sequence

from layers.layer_1_tools.level_1_impl.level_3.git_submodule_tool.tool import GitSubmoduleTool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="🔧 Git Submodule Tool")
    parser.add_argument(
        "--operation",
        choices=["sync", "push", "pull", "update"],
        default="sync",
        help="Operation to run (default: sync)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    tool = GitSubmoduleTool()
    ok = tool.run(operation=args.operation)
    return 0 if ok else 1

