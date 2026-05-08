# ============================================================
# writer.py — CSV output layer
# ============================================================

from pathlib import Path
import pandas as pd


def write_outputs(
    outputs: dict[str, pd.DataFrame],
    output_dir: Path,
) -> None:

    output_dir.mkdir(parents=True, exist_ok=True)

    for filename, df in outputs.items():
        df.to_csv(output_dir / filename, index=False)