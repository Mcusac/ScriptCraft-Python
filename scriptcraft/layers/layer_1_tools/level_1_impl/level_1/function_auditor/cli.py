
import argparse
import sys

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import build_arg_parser, run_cli_and_exit

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    FunctionAuditorTool,
)


def build_parser() -> argparse.ArgumentParser:
    parser = build_arg_parser(
        description="Function Usage Audit Tool",
        epilog="""
Examples:
  python -m scriptcraft.layers.layer_1_tools.level_1_impl.level_1.function_auditor.cli file.gd
  python -m scriptcraft.layers.layer_1_tools.level_1_impl.level_1.function_auditor.cli --batch --all
  python -m scriptcraft.layers.layer_1_tools.level_1_impl.level_1.function_auditor.cli --batch --folder scripts/Managers
  python -m scriptcraft.layers.layer_1_tools.level_1_impl.level_1.function_auditor.cli --batch --pattern "**/*Manager*.gd"
  python -m scriptcraft.layers.layer_1_tools.level_1_impl.level_1.function_auditor.cli --batch --extension py --base-folder src
  python -m scriptcraft.layers.layer_1_tools.level_1_impl.level_1.function_auditor.cli --batch --all --detailed-unused
        """,
    )

    parser.add_argument("file", nargs="?", help="Single file to audit")
    parser.add_argument("--batch", action="store_true", help="Run batch audit")
    parser.add_argument("--all", action="store_true", help="Audit all files")

    parser.add_argument("--managers", action="store_true", help="Audit manager files (deprecated - use --folder)")
    parser.add_argument("--ui", action="store_true", help="Audit UI files (deprecated - use --folder)")
    parser.add_argument("--utils", action="store_true", help="Audit utility files (deprecated - use --folder)")
    parser.add_argument("--factories", action="store_true", help="Audit factory files (deprecated - use --folder)")
    parser.add_argument("--coordinators", action="store_true", help="Audit coordinator files (deprecated - use --folder)")

    parser.add_argument("--folder", type=str, help='Audit files in specific folder (e.g., "scripts/Managers")')
    parser.add_argument("--extension", type=str, default="gd", help="File extension to audit (default: gd)")
    parser.add_argument("--pattern", type=str, help='Glob pattern to match files (e.g., "**/*Manager*.gd")')
    parser.add_argument("--base-folder", type=str, default="scripts", help="Base folder to search in (default: scripts)")

    parser.add_argument("--summary", action="store_true", help="Show only summary")
    parser.add_argument("--unused-only", action="store_true", help="Show only unused functions")
    parser.add_argument("--detailed-unused", action="store_true", help="Show detailed unused functions report")

    return parser


def resolve_batch_target(args: argparse.Namespace, batch_auditor) -> list[str]:
    if args.all:
        return batch_auditor.get_all_files()
    if args.pattern:
        return batch_auditor.get_files_by_pattern(args.pattern, args.base_folder)
    if args.folder:
        return batch_auditor.get_files_in_folder(args.folder)
    if args.extension != "gd" or args.base_folder != "scripts":
        return batch_auditor.get_files_by_extension(args.extension, args.base_folder)
    if args.managers:
        return batch_auditor.get_files_by_category("managers")
    if args.ui:
        return batch_auditor.get_files_by_category("ui")
    if args.utils:
        return batch_auditor.get_files_by_category("utils")
    if args.factories:
        return batch_auditor.get_files_by_category("factories")
    if args.coordinators:
        return batch_auditor.get_files_by_category("coordinators")
    return []


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.batch:
            tool = FunctionAuditorTool()
            tool.run(
                mode="batch",
                input_paths=None,
                output_dir=None,
                folder=args.folder,
                pattern=args.pattern,
                extension=args.extension,
                base_folder=args.base_folder,
                summary_only=args.summary,
                unused_only=args.unused_only,
                detailed_unused=args.detailed_unused,
            )
            return 0

        if args.file:
            tool = FunctionAuditorTool()
            tool.run(
                mode="single",
                input_paths=[Path(args.file)],
                output_dir=None,
                summary_only=args.summary,
                unused_only=args.unused_only,
                detailed_unused=args.detailed_unused,
            )
            return 0

        print("❌ No file specified. Use --help for options.")
        parser.print_help()
        return 2

    except KeyboardInterrupt:
        print("\n⏹️  Audit interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error during audit: {e}")
        return 1


if __name__ == "__main__":
    run_cli_and_exit(main, sys.argv[1:])

