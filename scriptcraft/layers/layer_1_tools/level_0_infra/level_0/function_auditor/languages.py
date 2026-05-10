"""Language-to-extension mapping used by the function auditor tool."""

from typing import Mapping

LANGUAGE_EXTENSIONS: Mapping[str, str] = {
    "python": "py",
    "gdscript": "gd",
    "javascript": "js",
    "typescript": "ts",
    "java": "java",
    "cpp": "cpp",
    "csharp": "cs",
}

DEFAULT_EXTENSION = "py"


def extension_for_language(language: str) -> str:
    """Return the canonical file extension for ``language`` (defaults to ``"py"``)."""
    if not isinstance(language, str):
        return DEFAULT_EXTENSION
    return LANGUAGE_EXTENSIONS.get(language.lower(), DEFAULT_EXTENSION)
