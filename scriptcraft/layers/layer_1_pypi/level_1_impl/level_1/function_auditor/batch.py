
from pathlib import Path
from typing import Any, Optional

from layers.layer_1_pypi.level_1_impl.level_0.function_auditor.auditor import FunctionAuditor


class BatchFunctionAuditor:
    """
    Audits multiple files for unused functions across multiple programming languages.

    This class provides batch processing capabilities for auditing entire
    folders or categories of files at once.
    """

    def __init__(self, project_root: Optional[str] = None, language: Optional[str] = None):
        self.language = language or "python"
        self.language_config = self._get_language_config()
        self.project_root = Path(project_root) if project_root else self._find_project_root()
        self.results: list[dict[str, Any]] = []

    def _get_language_config(self) -> dict[str, Any]:
        configs: dict[str, dict[str, Any]] = {
            "python": {
                "file_extensions": [".py"],
                "project_indicators": ["setup.py", "pyproject.toml", "requirements.txt", "__init__.py"],
            },
            "gdscript": {"file_extensions": [".gd"], "project_indicators": ["project.godot"]},
            "javascript": {"file_extensions": [".js"], "project_indicators": ["package.json", "node_modules"]},
            "typescript": {
                "file_extensions": [".ts"],
                "project_indicators": ["package.json", "tsconfig.json", "node_modules"],
            },
            "java": {"file_extensions": [".java"], "project_indicators": ["pom.xml", "build.gradle", "src"]},
            "cpp": {
                "file_extensions": [".cpp", ".c", ".h", ".hpp"],
                "project_indicators": ["CMakeLists.txt", "Makefile", "src"],
            },
            "csharp": {"file_extensions": [".cs"], "project_indicators": [".csproj", ".sln", "src"]},
        }
        return configs.get(self.language, configs["python"])

    def _find_project_root(self) -> Path:
        current = Path.cwd()
        indicators = self.language_config.get("project_indicators", [])
        while current != current.parent:
            for indicator in indicators:
                if (current / indicator).exists():
                    return current
            current = current.parent
        return Path(".")

    def get_files_by_category(self, category: str) -> list[Path]:
        """Get files by category (deprecated - use get_files_in_folder instead)."""
        base_path = self.project_root / "scripts"

        if category == "managers":
            return list(base_path.rglob("Managers/**/*.gd"))
        if category == "ui":
            return list(base_path.rglob("UI/**/*.gd"))
        if category == "utils":
            return list(base_path.rglob("Utils/**/*.gd"))
        if category == "factories":
            return list(base_path.rglob("Factories/**/*.gd"))
        if category == "coordinators":
            return list(base_path.rglob("Coordinators/**/*.gd"))
        return []

    def get_files_by_extension(self, extension: Optional[str] = None, base_folder: str = ".") -> list[Path]:
        """Get all files with specific extension in a base folder."""
        if extension is None:
            extensions = self.language_config["file_extensions"]
            files: list[Path] = []
            for ext in extensions:
                files.extend(list(self.project_root.rglob(f"**/*{ext}")))
            return files

        base_path = self.project_root / base_folder
        if not base_path.exists():
            return []
        return list(base_path.rglob(f"**/*.{extension}"))

    def get_files_by_pattern(self, pattern: str, base_folder: str = "scripts") -> list[Path]:
        """Get files matching a glob pattern in a base folder."""
        base_path = self.project_root / base_folder
        if not base_path.exists():
            return []
        return list(base_path.rglob(pattern))

    def get_files_in_folder(self, folder_path: str) -> list[Path]:
        """Get all files with language-specific extensions in a specific folder."""
        folder = self.project_root / folder_path
        if not folder.exists():
            print(f"❌ Folder not found: {folder}")
            return []

        extensions = self.language_config["file_extensions"]
        files: list[Path] = []
        for ext in extensions:
            files.extend(list(folder.rglob(f"*{ext}")))
        return files

    def get_all_files(self) -> list[Path]:
        """Get all files with language-specific extensions in the project."""
        extensions = self.language_config["file_extensions"]
        files: list[Path] = []
        for ext in extensions:
            files.extend(list(self.project_root.rglob(f"**/*{ext}")))
        return files

    def audit_files(
        self,
        files: list[Path],
        show_details: bool = True,
        unused_only: bool = False,
        verbose: bool = True,
    ) -> dict[str, Any]:
        if verbose:
            print(f"🔍 Starting batch audit of {len(files)} files...")
            print(f"📁 Project root: {self.project_root}")
            print("=" * 80)

        results: dict[str, Any] = {
            "files_audited": 0,
            "files_with_unused": 0,
            "total_functions": 0,
            "total_unused": 0,
            "file_results": [],
        }

        for i, file_path in enumerate(files, 1):
            if verbose:
                try:
                    rel = file_path.relative_to(self.project_root)
                except Exception:
                    rel = file_path
                print(f"\n[{i}/{len(files)}] Auditing: {rel}")

            try:
                auditor = FunctionAuditor(str(file_path), language=self.language)
                audit_result = auditor.audit_functions(verbose=False)

                file_result: dict[str, Any] = {
                    "file": str(file_path.relative_to(self.project_root)),
                    "unused_count": len(audit_result["unused"]),
                    "total_count": len(audit_result["unused"]) + len(audit_result["used"]),
                    "unused_functions": audit_result["unused"],
                    "used_functions": audit_result["used"],
                }

                results["file_results"].append(file_result)
                results["files_audited"] += 1
                results["total_functions"] += file_result["total_count"]
                results["total_unused"] += file_result["unused_count"]

                if file_result["unused_count"] > 0:
                    results["files_with_unused"] += 1

                if show_details and (not unused_only or file_result["unused_count"] > 0):
                    self._print_file_summary(file_result)
                    if file_result["unused_count"] > 0:
                        print("   🚨 UNUSED FUNCTIONS:")
                        for func in file_result["unused_functions"]:
                            print(f"      ❌ {func['name']} (line {func['line']})")
                        print()
            except Exception as e:
                if verbose:
                    print(f"   ❌ Error auditing file: {e}")
                continue

        return results

    def _print_file_summary(self, file_result: dict[str, Any]) -> None:
        unused = file_result["unused_count"]
        total = file_result["total_count"]
        status = "❌" if unused > 0 else "✅"
        print(f"   {status} {total} functions, {unused} unused")

    def get_unused_functions_list(self, results: dict[str, Any]) -> list[dict[str, Any]]:
        unused_functions: list[dict[str, Any]] = []
        for file_result in results["file_results"]:
            if file_result["unused_count"] > 0:
                for func in file_result["unused_functions"]:
                    unused_functions.append(
                        {"file": file_result["file"], "function": func["name"], "line": func["line"]}
                    )
        return unused_functions

    def generate_batch_report(self, results: dict[str, Any], verbose: bool = True) -> None:
        if not verbose:
            return

        print("\n" + "=" * 80)
        print("📊 BATCH FUNCTION USAGE AUDIT REPORT")
        print("=" * 80)

        print(f"📁 Project: {self.project_root}")
        print(f"📋 Files audited: {results['files_audited']}")
        print(f"🚨 Files with unused functions: {results['files_with_unused']}")
        print(f"📊 Total functions: {results['total_functions']}")
        print(f"❌ Total unused functions: {results['total_unused']}")

        if results["total_functions"] > 0:
            unused_percentage = (results["total_unused"] / results["total_functions"]) * 100
            print(f"📈 Unused function percentage: {unused_percentage:.1f}%")

        print()

        if results["files_with_unused"] > 0:
            print("🚨 FILES WITH UNUSED FUNCTIONS:")
            print("-" * 50)
            for file_result in results["file_results"]:
                if file_result["unused_count"] > 0:
                    print(f"   ❌ {file_result['file']} ({file_result['unused_count']} unused)")
                    unused_names = [func["name"] for func in file_result["unused_functions"]]
                    print(f"      Functions: {', '.join(unused_names)}")
            print()

            print("💡 RECOMMENDATIONS:")
            print("-" * 50)
            print("   • Review each file with unused functions")
            print("   • Consider if functions are planned for future use")
            print("   • Comment out with clear markers if keeping")
            print("   • Delete if truly unnecessary")
            print("   • Use the individual audit script for detailed analysis")
            print()

        clean_files = results["files_audited"] - results["files_with_unused"]
        if clean_files > 0:
            print(f"✅ CLEAN FILES ({clean_files}):")
            print("-" * 50)
            for file_result in results["file_results"]:
                if file_result["unused_count"] == 0:
                    print(f"   ✅ {file_result['file']}")
            print()

    def generate_unused_functions_report(self, results: dict[str, Any], verbose: bool = True):
        unused_functions = self.get_unused_functions_list(results)

        if not verbose:
            return unused_functions

        print("\n" + "=" * 80)
        print("📋 DETAILED UNUSED FUNCTIONS REPORT")
        print("=" * 80)

        if not unused_functions:
            print("🎉 No unused functions found!")
            return unused_functions

        print(f"📊 Total unused functions: {len(unused_functions)}")
        print()

        files_with_unused: dict[str, list[dict[str, Any]]] = {}
        for func in unused_functions:
            file_path = func["file"]
            files_with_unused.setdefault(file_path, []).append(func)

        for file_path, functions in files_with_unused.items():
            print(f"📁 {file_path} ({len(functions)} unused):")
            for func in functions:
                print(f"   ❌ {func['function']} (line {func['line']})")
            print()

        return unused_functions

