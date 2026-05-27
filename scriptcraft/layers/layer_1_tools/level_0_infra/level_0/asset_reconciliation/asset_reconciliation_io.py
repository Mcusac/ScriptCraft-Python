"""Temporary infra home for reconciliation I/O helpers.

Candidate for future extraction into layer_0_core file I/O utilities.
"""

import pandas as pd

from pathlib import Path

from scriptcraft.layers.layer_0_core.level_4.file_io.csv import save_csv


def write_outputs(
    outputs: dict[str, pd.DataFrame],
    output_dir: Path,
) -> None:
    for filename, df in outputs.items():
        save_csv(df, output_dir / filename, index=False)
