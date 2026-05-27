from pathlib import Path
from typing import Any, Dict, List, Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    ProjectRootFinder,
    LanguageDetector,
    LanguageConfig,
    UsageSearcher,
    AuditorReporter,
    FunctionExtractor,
)


class FunctionAuditor:
    """Thin orchestration layer (SOLID)."""

    def __init__(self, target_file: str, language: Optional[str] = None):
        self.target_file = Path(target_file)

        self.language = language or LanguageDetector.detect(self.target_file)
        self.config = LanguageConfig.get(self.language)

        self.project_root = ProjectRootFinder.find(
            self.target_file.parent,
            self.config.get("project_indicators", []),
        )

        self.extractor = FunctionExtractor(self.config, self.language)
        self.searcher = UsageSearcher(self.project_root, self.config, self.target_file)

    def audit(self, verbose: bool = True) -> Dict[str, List[Dict[str, Any]]]:
        if not self.target_file.exists():
            return {"unused": [], "used": []}

        content = self.target_file.read_text(encoding="utf-8")

        functions = self.extractor.extract(content)

        unused = []
        used = []

        for func in functions:
            usage = self.searcher.search(func["name"])

            if usage:
                used.append({"function": func, "usage": usage})
            else:
                unused.append(func)

        result = {"unused": unused, "used": used}

        if verbose:
            AuditorReporter.print_report(self.target_file, self.project_root, result)

        return result