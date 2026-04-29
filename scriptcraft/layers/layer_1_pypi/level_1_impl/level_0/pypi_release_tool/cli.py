from __future__ import annotations

import argparse
from collections.abc import Sequence

from .tool import PyPIReleaseTool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="📦 PyPI Release Tool")
    parser.add_argument(
        "--operation",
        choices=["test", "release", "validate", "build"],
        default="test",
        help="Operation to run (default: test)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    tool = PyPIReleaseTool()
    ok = tool.run(operation=args.operation)
    raise SystemExit(0 if ok else 1)

