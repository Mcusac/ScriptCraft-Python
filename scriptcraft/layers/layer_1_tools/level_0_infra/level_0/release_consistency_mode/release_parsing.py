"""
Release parsing utilities.
"""

import re

from pathlib import Path
from typing import List, Optional, Tuple


def extract_release_number(name: str, pattern: str) -> Optional[int]:
    match = re.search(pattern, name)
    return int(match.group(1)) if match else None


def extract_generic_release(name: str, patterns: List[str]) -> str:
    for pattern in patterns:
        m = re.search(pattern, name)
        if m:
            return m.group(1) if m.lastindex else m.group(0)
    return "unknown"


def pick_highest_release(files: List[Tuple[int, Path]]) -> Optional[Path]:
    return max(files, key=lambda x: x[0])[1] if files else None