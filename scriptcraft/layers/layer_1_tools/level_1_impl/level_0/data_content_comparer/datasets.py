
from pathlib import Path
from typing import List, Union

import pandas as pd

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_data


def load_datasets_as_list(input_paths: List[Union[str, Path]]) -> List[pd.DataFrame]:
    """Load multiple datasets from the provided paths."""
    datasets: List[pd.DataFrame] = []
    for path in input_paths:
        try:
            df = load_data(path)
            if df is not None:
                datasets.append(df)
            else:
                log_and_print(f"⚠️ Warning: Failed to load dataset from {path}")
        except Exception as e:
            log_and_print(f"❌ Error loading dataset from {path}: {e}")

    return datasets

