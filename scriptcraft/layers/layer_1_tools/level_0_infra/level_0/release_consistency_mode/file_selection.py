"""
File selection utilities.

Single responsibility:
- Find files using patterns
- Filter by exclusions
"""

from pathlib import Path
from typing import List, Optional


def select_files(root: Path, patterns: List[str], exclude_prefixes: Optional[List[str]] = None) -> List[Path]:
    exclude_prefixes = exclude_prefixes or []

    def valid(p: Path) -> bool:
        return not any(p.name.startswith(x) for x in exclude_prefixes)

    results = []
    for pattern in patterns:
        for f in root.glob(pattern):
            if valid(f):
                results.append(f)

    return results


def find_first_match(root: Path, primary: str, fallback: List[str], exclude_prefixes: Optional[List[str]] = None) -> Optional[Path]:
    primary_path = root / primary
    if primary_path.exists():
        return primary_path

    candidates = select_files(root, fallback, exclude_prefixes)
    return candidates[0] if candidates else None