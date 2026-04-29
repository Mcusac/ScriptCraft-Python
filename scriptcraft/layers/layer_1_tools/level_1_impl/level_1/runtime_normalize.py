"""
Small normalization helpers.
"""

from pathlib import Path
from typing import List, Optional, Sequence, Union

from layers.layer_1_pypi.level_1_impl.level_0.runtime.protocols import PathLike


def normalize_list(value: Optional[Union[PathLike, Sequence[PathLike]]]) -> List[PathLike]:
    """Normalize None/str/Path/list-like into a list."""
    if value is None:
        return []
    if isinstance(value, (str, Path)):
        return [value]
    return list(value)

