import re

from typing import Any, Dict, List, Optional


class FunctionExtractor:
    """Extract functions from file content."""

    def __init__(self, config: Dict[str, Any], language: str):
        self.config = config
        self.language = language

    def extract(self, content: str) -> List[Dict[str, Any]]:
        pattern = self.config["function_pattern"]
        builtin = self.config["builtin_functions"]
        private_prefix = self.config["private_prefix"]

        functions: List[Dict[str, Any]] = []

        for i, line in enumerate(content.split("\n"), 1):
            match = re.match(pattern, line)
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

            if func_name in builtin:
                continue

            functions.append({
                "name": func_name,
                "line": i,
                "indent": len(indent),
                "is_static": "static" in line,
                "is_private": func_name.startswith(private_prefix),
                "language": self.language,
            })

        return functions

    @staticmethod
    def _is_public_api(func_name: str) -> bool:
        return any(func_name.startswith(p) for p in ["_on_", "_handle_", "_process_", "_update_"])