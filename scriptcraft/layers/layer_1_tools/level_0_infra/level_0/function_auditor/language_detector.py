from pathlib import Path


class LanguageDetector:
    """Detect programming language from file extension."""

    LANGUAGE_MAP = {
        ".py": "python",
        ".gd": "gdscript",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "cpp",
        ".cs": "csharp",
    }

    @classmethod
    def detect(cls, file_path: Path) -> str:
        return cls.LANGUAGE_MAP.get(file_path.suffix.lower(), "python")