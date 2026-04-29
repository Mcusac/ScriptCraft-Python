"""Path helpers shared across automated labeler modes."""

from pathlib import Path
from typing import Optional


def resolve_output_file(
    output_path: Path,
    output_filename: Optional[str],
    default_name: str,
) -> Path:
    """Return ``output_path / output_filename`` if provided, else fall back to ``default_name``."""
    return output_path / (output_filename or default_name)
