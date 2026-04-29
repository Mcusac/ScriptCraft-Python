#!/usr/bin/env python3
"""
Standalone entrypoint for the Generic Release Tool.

This exists to support running the tool directly from the repository without
installing the package, while keeping `generic_release_tool_main.py` deleted.
"""

from layers.layer_1_pypi.level_1_impl.level_3.generic_release_tool.cli import main as cli_main


def main() -> None:
    # When run by file path, `layers.*` imports require the `scriptcraft/` dir
    # to be on `sys.path`.
    import sys
    from pathlib import Path

    scriptcraft_dir = Path(__file__).resolve().parents[5]
    sys.path.insert(0, str(scriptcraft_dir))

    cli_main()


if __name__ == "__main__":
    main()

