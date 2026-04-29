
from pathlib import Path
from typing import Union

import pandas as pd


def save_labeled_data(data: pd.DataFrame, output_path: Union[str, Path], *, format: str = "excel") -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format.lower() == "excel":
        data.to_excel(output_path, index=False)
        return

    data.to_csv(output_path, index=False)

