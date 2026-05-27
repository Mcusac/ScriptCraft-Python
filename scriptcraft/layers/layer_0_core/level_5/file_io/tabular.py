"""Tabular file loading (CSV via core; Excel via pandas)."""

import pandas as pd

from pathlib import Path
from typing import Any, Optional, Sequence, Tuple, Union

from scriptcraft.layers.layer_0_core.level_4 import load_csv_raw

PathLike = Union[str, Path]


def load_tabular(
    file_path: PathLike,
    encoding: Optional[str] = None,
    **kwargs: Any,
) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        return load_csv_raw(path, encoding=encoding, **kwargs)
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(path, **kwargs)
    raise ValueError(f"Unsupported file format: {suffix}")


def load_comparison_pair(
    file_paths: Sequence[PathLike],
    encoding: Optional[str] = None,
    **kwargs: Any,
) -> Tuple[pd.DataFrame, pd.DataFrame, str]:
    """Load exactly two tabular files; dataset name is the first file stem."""
    paths = [Path(p) for p in file_paths]
    if len(paths) != 2:
        raise ValueError(f"Expected 2 input files, got {len(paths)}")
    df1 = load_tabular(paths[0], encoding=encoding, **kwargs)
    df2 = load_tabular(paths[1], encoding=encoding, **kwargs)
    return df1, df2, paths[0].stem
