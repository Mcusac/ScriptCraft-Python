
import argparse
import sys

from layers.layer_1_tools.level_1_impl.level_0.function_auditor.auditor import FunctionAuditor
from layers.layer_1_tools.level_1_impl.level_1.function_auditor.batch import BatchFunctionAuditor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Function Usage Audit Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m scriptcraft.layers.layer_1_pypi.level_1_impl.level_0.function_auditor.cli file.gd
  python -m scriptcraft.layers.layer_1_pypi.level_1_impl.level_0.function_auditor.cli --batch --all
  python -m scriptcraft.layers.layer_1_pypi.level_1_impl.level_0.function_auditor.cli --batch --folder scripts/Managers
  python -m scriptcraft.layers.layer_1_pypi.level_1_impl.level_0.function_auditor.cli --batch --pattern "**/*Manager*.gd"
  python -m scriptcraft.layers.layer_1_pypi.level_1_impl.level_0.function_auditor.cli --batch --extension py --base-folder src
  python -m scriptcraft.layers.layer_1_pypi.level_1_impl.level_0.function_auditor.cli --batch --all --detailed-unused
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


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.batch:
            batch_auditor = BatchFunctionAuditor()

            if args.all:
                files = batch_auditor.get_all_files()
            elif args.pattern:
                files = batch_auditor.get_files_by_pattern(args.pattern, args.base_folder)
            elif args.folder:
                files = batch_auditor.get_files_in_folder(args.folder)
            elif args.extension != "gd" or args.base_folder != "scripts":
                files = batch_auditor.get_files_by_extension(args.extension, args.base_folder)
            elif args.managers:
                files = batch_auditor.get_files_by_category("managers")
            elif args.ui:
                files = batch_auditor.get_files_by_category("ui")
            elif args.utils:
                files = batch_auditor.get_files_by_category("utils")
            elif args.factories:
                files = batch_auditor.get_files_by_category("factories")
            elif args.coordinators:
                files = batch_auditor.get_files_by_category("coordinators")
            else:
                print("❌ No batch audit target specified")
                print("💡 Use --folder, --pattern, --extension, or --all")
                return 2

            if not files:
                print("❌ No files found to audit")
                return 2

            results = batch_auditor.audit_files(files, show_details=not args.summary, unused_only=args.unused_only)
            batch_auditor.generate_batch_report(results)

            if args.detailed_unused:
                batch_auditor.generate_unused_functions_report(results)

            return 0

        if args.file:
            auditor = FunctionAuditor(args.file)
            result = auditor.audit_functions()
            auditor.generate_report(result)
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
    raise SystemExit(main(sys.argv[1:]))

