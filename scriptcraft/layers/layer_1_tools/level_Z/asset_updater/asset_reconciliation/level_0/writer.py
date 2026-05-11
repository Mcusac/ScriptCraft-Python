# ============================================================
# writer.py — CSV output layer
# ============================================================

import pandas as pd

from pathlib import Path


def write_outputs(
    outputs: dict[str, pd.DataFrame],
    output_dir: Path,
) -> None:

    output_dir.mkdir(parents=True, exist_ok=True)

    for filename, df in outputs.items():
        df.to_csv(output_dir / filename, index=False)