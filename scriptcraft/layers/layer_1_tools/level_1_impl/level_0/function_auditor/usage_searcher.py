import re
from pathlib import Path
from typing import Any, Dict, List


class UsageSearcher:
    """Search for function usage across project."""

    def __init__(self, project_root: Path, config: Dict[str, Any], target_file: Path):
        self.project_root = project_root
        self.config = config
        self.target_file = target_file

    def search(self, func_name: str) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        files = []
        for ext in self.config["file_extensions"]:
            files.extend(self.project_root.rglob(f"*{ext}"))

        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue

            for i, line in enumerate(content.split("\n"), 1):
                if self._is_definition_line(file_path, line, func_name):
                    continue

                if self._is_call(line, func_name):
                    results.append({
                        "file": str(file_path.relative_to(self.project_root)),
                        "line": i,
                        "content": line.strip(),
                    })

        return results

    def _is_definition_line(self, file_path: Path, line: str, func_name: str) -> bool:
        return file_path == self.target_file and f"{func_name}(" in line

    @staticmethod
    def _is_call(line: str, func_name: str) -> bool:
        line = re.sub(r"#.*$", "", line)

        patterns = [
            rf"\b{func_name}\s*\(",
            rf"\.{func_name}\s*\(",
            rf"{func_name}\.connect",
            rf"connect\s*\(\s*{func_name}",
        ]

        return any(re.search(p, line) for p in patterns)