"""
Reporting layer.
"""
import pandas as pd

from pathlib import Path
from typing import Set

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print


def write_csv(df: pd.DataFrame, path: Path, dataset: str, message: str):
    path.mkdir(parents=True, exist_ok=True)
    out = path / f"{dataset}.csv"
    df.to_csv(out)
    log_and_print(f"📁 {message}: {out}")


def column_changes(old: Set[str], new: Set[str], dataset: str):
    if old or new:
        log_and_print(f"📊 Column changes: {dataset}")
        if old:
            log_and_print(f"🗑️ Removed: {sorted(old)}")
        if new:
            log_and_print(f"➕ Added: {sorted(new)}")
    else:
        log_and_print(f"✅ No column changes: {dataset}")