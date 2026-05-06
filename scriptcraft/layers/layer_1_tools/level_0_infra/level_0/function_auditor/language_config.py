from typing import Any, Dict


class LanguageConfig:
    """Provides language-specific configurations."""

    CONFIGS: Dict[str, Dict[str, Any]] = {
        "python": {
            "function_pattern": r"^(\s*)def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(",
            "file_extensions": [".py"],
            "builtin_functions": [
                "__init__", "__str__", "__repr__", "__len__",
                "__getitem__", "__setitem__",
            ],
            "private_prefix": "_",
            "project_indicators": [
                "setup.py", "pyproject.toml",
                "requirements.txt", "__init__.py",
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

    @classmethod
    def get(cls, language: str) -> Dict[str, Any]:
        return cls.CONFIGS.get(language, cls.CONFIGS["python"])