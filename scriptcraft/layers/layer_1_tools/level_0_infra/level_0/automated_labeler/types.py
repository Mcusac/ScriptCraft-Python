"""Small types used by the automated labeler tool."""
import pandas as pd

from pathlib import Path
from typing import Any, Dict, Protocol

from scriptcraft.layers.layer_0_core.level_0.runtime import InputPath, InputPaths

LabelingRules = Dict[str, Any]


class LoaderSaver(Protocol):
    """Narrow I/O contract that mode functions need from the tool."""

    def load_data_file(self, path: InputPath) -> pd.DataFrame: ...

    def save_data_file(
        self,
        df: pd.DataFrame,
        output: Path,
        *,
        include_index: bool = ...,
    ) -> None: ...
