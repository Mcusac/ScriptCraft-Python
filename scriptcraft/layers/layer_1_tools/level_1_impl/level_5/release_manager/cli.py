
from typing import Sequence

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    parse_release_manager_argv,
    run_cli_and_exit,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_3 import ReleaseManager
from scriptcraft.layers.layer_1_tools.level_1_impl.level_4 import print_release_manager_help


def main(argv: Sequence[str] | None = None) -> int:
    if not argv:
        print_release_manager_help()
        return 0

    mode = str(argv[0]).lower()
    if mode in ["--help", "-h", "help"]:
        print_release_manager_help()
        return 0

    parsed = parse_release_manager_argv(argv)
    tool = ReleaseManager()
    try:
        tool.run(**parsed.kwargs)
        return 0
    except Exception:
        return 1

if __name__ == "__main__":
    run_cli_and_exit(main)
