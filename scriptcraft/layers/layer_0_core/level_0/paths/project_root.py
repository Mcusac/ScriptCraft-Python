"""Find project root using marker files."""

from pathlib import Path
from typing import List


class ProjectRootFinder:
    """Find project root using indicator files."""

    @staticmethod
    def find(start: Path, indicators: List[str]) -> Path:
        current = start

        while current != current.parent:
            for indicator in indicators:
                if (current / indicator).exists():
                    return current
            current = current.parent

        return Path(".")
