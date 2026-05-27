#!/usr/bin/env python3
"""
Standalone entrypoint for the Generic Release Tool.

Supports running the tool directly from the repository without installing
the package, while keeping legacy top-level script names removed.
"""

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    main as cli_main,
)


def main() -> None:
    import sys
    from pathlib import Path

    scriptcraft_dir = Path(__file__).resolve().parents[5]
    sys.path.insert(0, str(scriptcraft_dir))

    cli_main()


if __name__ == "__main__":
    main()
