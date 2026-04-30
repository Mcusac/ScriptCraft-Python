from layers.layer_1_tools.level_1_impl.level_0.function_auditor.auditor import FunctionAuditor
from layers.layer_1_tools.level_1_impl.level_1.function_auditor.batch import BatchFunctionAuditor


def example_single_file_audit() -> None:
    print("🔍 Example: Single File Audit")
    print("=" * 50)

    auditor = FunctionAuditor("scripts/Managers/Construction/BuildingManager.gd")
    result = auditor.audit_functions(verbose=False)

    print(f"Found {len(result['unused'])} unused functions")
    for func in result["unused"]:
        print(f"  ❌ {func['name']} (line {func['line']})")
    print()


def example_batch_audit() -> None:
    print("🔍 Example: Batch Audit")
    print("=" * 50)

    batch_auditor = BatchFunctionAuditor()

    print("Method 1: Audit specific folder")
    files = batch_auditor.get_files_in_folder("scripts/Managers/Construction")
    results = batch_auditor.audit_files(files, show_details=False, verbose=False)
    print(f"Audited {results['files_audited']} files, found {results['total_unused']} unused functions")
    print()

    print("Method 2: Audit files matching pattern")
    files = batch_auditor.get_files_by_pattern("**/*Manager*.gd", "scripts")
    results = batch_auditor.audit_files(files, show_details=False, verbose=False)
    print(f"Audited {results['files_audited']} files, found {results['total_unused']} unused functions")
    print()

    print("Method 3: Audit files by extension")
    files = batch_auditor.get_files_by_extension("gd", "scripts")
    results = batch_auditor.audit_files(files, show_details=False, verbose=False)
    print(f"Audited {results['files_audited']} files, found {results['total_unused']} unused functions")
    print()


def example_get_unused_functions() -> None:
    print("🔍 Example: Get Unused Functions Data")
    print("=" * 50)

    batch_auditor = BatchFunctionAuditor()

    files = batch_auditor.get_files_in_folder("scripts/Managers/Construction")
    results = batch_auditor.audit_files(files, show_details=False, verbose=False)

    unused_functions = batch_auditor.get_unused_functions_list(results)

    print(f"Found {len(unused_functions)} unused functions:")
    for func in unused_functions:
        print(f"  📁 {func['file']}")
        print(f"     ❌ {func['function']} (line {func['line']})")
    print()


def example_custom_project() -> None:
    print("🔍 Example: Custom Project Structure")
    print("=" * 50)

    batch_auditor = BatchFunctionAuditor()

    files = batch_auditor.get_files_by_extension("py", ".")
    if files:
        results = batch_auditor.audit_files(files, show_details=False, verbose=False)
        print(f"Found {len(files)} Python files, {results['total_unused']} unused functions")
    else:
        print("No Python files found in current directory")
    print()


def main() -> int:
    print("🚀 ScriptCraft Function Auditor Plugin Examples")
    print("=" * 60)
    print()

    try:
        example_single_file_audit()
        example_batch_audit()
        example_get_unused_functions()
        example_custom_project()

        print("✅ All examples completed successfully!")
        print()
        print("💡 Integration Tips:")
        print("  • Use verbose=False for programmatic usage")
        print("  • Use get_unused_functions_list() for structured data")
        print("  • Use get_files_by_pattern() for flexible file selection")
        print("  • Use get_files_by_extension() for different file types")
        return 0
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("💡 Make sure you're running this from the project root directory")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

