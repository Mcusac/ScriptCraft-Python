
from typing import Sequence

from layers.layer_1_pypi.level_1_impl.level_0.release_manager.argv_compat import parse_release_manager_argv
from layers.layer_1_pypi.level_1_impl.level_2.release_manager.tool import ReleaseManager
from layers.layer_1_pypi.level_1_impl.level_3.release_manager.help_text import print_release_manager_help


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
    raise SystemExit(main())
s