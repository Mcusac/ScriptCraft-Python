"""
Small normalization helpers.
"""

from pathlib import Path
from typing import List, Optional, Sequence, Union

from scriptcraft.layers.layer_0_core.level_0.runtime.tool_protocols import PathLike


def normalize_list(
    value: Optional[Union[PathLike, Sequence[PathLike]]],
) -> List[PathLike]:
    """Normalize None/str/Path/list-like into a list."""
    if value is None:
        return []
    if isinstance(value, (str, Path)):
        return [value]
    return list(value)
