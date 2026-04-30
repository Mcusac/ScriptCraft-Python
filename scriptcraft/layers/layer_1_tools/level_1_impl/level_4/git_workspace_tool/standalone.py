#!/usr/bin/env python3
"""
Standalone entrypoint for the Git Workspace Tool.

Supports running from the repository without installing the package.
"""
from layers.layer_1_tools.level_1_impl.level_3.git_workspace_tool.cli import main as cli_main


def main() -> None:
    import sys
    from pathlib import Path

    scriptcraft_dir = Path(__file__).resolve().parents[5]
    sys.path.insert(0, str(scriptcraft_dir))

    cli_main()


if __name__ == "__main__":
    main()

