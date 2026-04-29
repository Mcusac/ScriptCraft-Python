
import re

from pathlib import Path
from typing import Any, Optional


class FunctionAuditor:
    """
    Audits individual files for unused functions across multiple programming languages.

    This class extracts function definitions and searches for their usage
    across the entire codebase to identify potentially unused functions.
    Supports Python, GDScript, JavaScript, TypeScript, Java, C++, and C#.
    """

    def __init__(self, target_file: str, language: Optional[str] = None):
        self.target_file = Path(target_file)
        self.language = language or self._detect_language()
        self.language_config = self._get_language_config()
        self.project_root = self._find_project_root()
        self.functions: list[dict[str, Any]] = []
        self.unused_functions: list[dict[str, Any]] = []

    def _detect_language(self) -> str:
        """Detect programming language from file extension."""
        extension = self.target_file.suffix.lower()
        language_map = {
            ".py": "python",
            ".gd": "gdscript",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "cpp",
            ".cs": "csharp",
        }
        return language_map.get(extension, "python")

    def _get_language_config(self) -> dict[str, Any]:
        """Get language-specific configuration."""
        configs: dict[str, dict[str, Any]] = {
            "python": {
                "function_pattern": r"^(\s*)def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(",
                "file_extensions": [".py"],
                "builtin_functions": [
                    "__init__",
                    "__str__",
                    "__repr__",
                    "__len__",
                    "__getitem__",
                    "__setitem__",
                ],
                "private_prefix": "_",
                "project_indicators": [
                    "setup.py",
                    "pyproject.toml",
                    "requirements.txt",
                    "__init__.py",
                ],
            },
            "gdscript": {
                "function_pattern": r"^(\s*)func\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?:->\s*[^:]+)?\s*:",
                "file_extensions": [".gd"],
                "builtin_functions": ["_ready", "_process", "_input", "_exit_tree", "_enter_tree"],
                "private_prefix": "_",
                "project_indicators": ["project.godot"],
            },
            "javascript": {
                "function_pattern": r"^(\s*)(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)|(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:function|\([^)]*\)\s*=>))",
                "file_extensions": [".js"],
                "builtin_functions": [],
                "private_prefix": "_",
                "project_indicators": ["package.json", "node_modules"],
            },
            "typescript": {
                "function_pattern": r"^(\s*)(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)|(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:function|\([^)]*\)\s*=>)|([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*:\s*[^{]*\s*{)",
                "file_extensions": [".ts"],
                "builtin_functions": [],
                "private_prefix": "_",
                "project_indicators": ["package.json", "tsconfig.json", "node_modules"],
            },
            "java": {
                "function_pattern": r"^(\s*)(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:[a-zA-Z_][a-zA-Z0-9_]*\s+)*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(",
                "file_extensions": [".java"],
                "builtin_functions": ["main", "toString", "equals", "hashCode"],
                "private_prefix": "_",
                "project_indicators": ["pom.xml", "build.gradle", "src"],
            },
            "cpp": {
                "function_pattern": r"^(\s*)(?:[a-zA-Z_][a-zA-Z0-9_]*\s+)*([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?:const\s*)?\s*{",
                "file_extensions": [".cpp", ".c", ".h", ".hpp"],
                "builtin_functions": ["main"],
                "private_prefix": "_",
                "project_indicators": ["CMakeLists.txt", "Makefile", "src"],
            },
            "csharp": {
                "function_pattern": r"^(\s*)(?:public|private|protected|internal)?\s*(?:static\s+)?(?:[a-zA-Z_][a-zA-Z0-9_]*\s+)*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(",
                "file_extensions": [".cs"],
                "builtin_functions": ["Main", "ToString", "Equals", "GetHashCode"],
                "private_prefix": "_",
                "project_indicators": [".csproj", ".sln", "src"],
            },
        }
        return configs.get(self.language, configs["python"])

    def _find_project_root(self) -> Path:
        """Find the project root by looking for language-specific indicators."""
        current = self.target_file.parent
        indicators = self.language_config.get("project_indicators", [])

        while current != current.parent:
            for indicator in indicators:
                if (current / indicator).exists():
                    return current
            current = current.parent

        return Path(".")

    def extract_functions(self) -> list[dict[str, Any]]:
        """Extract all function definitions from the target file."""
        if not self.target_file.exists():
            print(f"❌ File not found: {self.target_file}")
            return []

        content = self.target_file.read_text(encoding="utf-8")

        func_pattern = self.language_config["function_pattern"]
        builtin_functions = self.language_config["builtin_functions"]
        private_prefix = self.language_config["private_prefix"]

        functions: list[dict[str, Any]] = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            match = re.match(func_pattern, line)
            if not match:
                continue

            indent = match.group(1)

            func_name: Optional[str] = None
            for group in match.groups()[1:]:
                if group:
                    func_name = group
                    break
            if not func_name:
                continue

            if func_name.startswith(private_prefix) and not self._is_public_api(func_name):
                continue

            if func_name in builtin_functions:
                continue

            functions.append(
                {
                    "name": func_name,
                    "line": i,
                    "indent": len(indent),
                    "is_static": "static" in line,
                    "is_private": func_name.startswith(private_prefix),
                    "language": self.language,
                }
            )

        self.functions = functions
        return functions

    def _is_public_api(self, func_name: str) -> bool:
        """Check if a private function is actually public API (like signal handlers)."""
        signal_handlers = ["_on_", "_handle_", "_process_", "_update_"]
        return any(func_name.startswith(prefix) for prefix in signal_handlers)

    def _is_function_call(self, line: str, func_name: str) -> bool:
        """Check if a line contains a call to the function."""
        line = re.sub(r"#.*$", "", line)

        patterns = [
            rf"\b{func_name}\s*\(",
            rf"\.{func_name}\s*\(",
            rf"{func_name}\.connect",
            rf"connect\s*\(\s*{func_name}",
        ]

        return any(re.search(pattern, line) for pattern in patterns)

    def search_function_usage(self, func_name: str) -> list[dict[str, Any]]:
        """Search for usage of a function across the entire codebase."""
        usage_locations: list[dict[str, Any]] = []

        extensions = self.language_config["file_extensions"]
        search_files: list[Path] = []
        for ext in extensions:
            search_files.extend(list(self.project_root.rglob(f"*{ext}")))

        for file_path in search_files:
            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"⚠️  Warning: Could not read {file_path}: {e}")
                continue

            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if file_path == self.target_file and f"func {func_name}(" in line:
                    continue

                if self._is_function_call(line, func_name):
                    usage_locations.append(
                        {
                            "file": str(file_path.relative_to(self.project_root)),
                            "line": i,
                            "content": line.strip(),
                        }
                    )

        return usage_locations

    def audit_functions(self, verbose: bool = True) -> dict[str, list[dict[str, Any]]]:
        """Perform the complete audit."""
        if verbose:
            try:
                rel = self.target_file.relative_to(self.project_root)
            except Exception:
                rel = self.target_file
            print(f"🔍 Auditing functions in: {rel}")
            print(f"📁 Project root: {self.project_root}")
            print()

        functions = self.extract_functions()
        if not functions:
            if verbose:
                print("❌ No functions found in file")
            return {"unused": [], "used": []}

        if verbose:
            print(f"📋 Found {len(functions)} functions to audit:")
            for func in functions:
                print(f"   - {func['name']} (line {func['line']})")
            print()

        unused: list[dict[str, Any]] = []
        used: list[dict[str, Any]] = []

        for func in functions:
            if verbose:
                print(f"🔍 Checking usage of: {func['name']}")

            usage = self.search_function_usage(func["name"])
            if usage:
                used.append({"function": func, "usage": usage})
                if verbose:
                    print(f"   ✅ Used {len(usage)} times")
                    for use in usage[:3]:
                        print(f"      - {use['file']}:{use['line']}")
                    if len(usage) > 3:
                        print(f"      ... and {len(usage) - 3} more")
            else:
                unused.append(func)
                if verbose:
                    print("   ❌ UNUSED")

        if verbose:
            print()

        return {"unused": unused, "used": used}

    def generate_report(self, audit_result: dict[str, list[dict[str, Any]]], verbose: bool = True) -> None:
        """Generate a detailed report."""
        if not verbose:
            return

        unused = audit_result["unused"]
        used = audit_result["used"]

        print("=" * 80)
        print("📊 FUNCTION USAGE AUDIT REPORT")
        print("=" * 80)
        try:
            rel = self.target_file.relative_to(self.project_root)
        except Exception:
            rel = self.target_file
        print(f"📁 File: {rel}")
        print(f"📋 Total functions: {len(unused) + len(used)}")
        print(f"✅ Used functions: {len(used)}")
        print(f"❌ Unused functions: {len(unused)}")
        print()

        if unused:
            print("🚨 UNUSED FUNCTIONS:")
            print("-" * 40)
            for func in unused:
                print(f"   ❌ {func['name']} (line {func['line']})")
            print()

            print("💡 RECOMMENDATIONS:")
            print("-" * 40)
            print("   • Review each unused function")
            print("   • Consider if it's planned for future use")
            print("   • Comment out with clear markers if keeping")
            print("   • Delete if truly unnecessary")
            print()

        if used:
            print("✅ USED FUNCTIONS:")
            print("-" * 40)
            for item in used:
                func = item["function"]
                usage = item["usage"]
                print(f"   ✅ {func['name']} (line {func['line']}) - used {len(usage)} times")
            print()

