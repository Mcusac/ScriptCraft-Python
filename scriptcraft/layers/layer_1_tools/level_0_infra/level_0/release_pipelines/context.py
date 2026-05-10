from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class ReleasePipelineContext:
    version: str = "0.0.0"
    dry_run: bool = False
    repo_root: Optional[Path] = None
    package_root: Optional[Path] = None
    docs_root: Optional[Path] = None
    timestamp: Optional[str] = None
    extras: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default=None):
        return self.extras.get(key, default)