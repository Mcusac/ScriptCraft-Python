# ============================================================
# form_utils.py — shared utilities (pure helpers)
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import FORM_RAW


def safe_get(row: pd.Series, col: str):
    return row.get(col) if col in row.index else None


def build_full_name(row: pd.Series) -> str:
    first = str(safe_get(row, FORM_RAW.first_name) or "").strip()
    last = str(safe_get(row, FORM_RAW.last_name) or "").strip()
    return f"{first} {last}".strip()


def resolve_column(base: str, suffix: int) -> str:
    return base if suffix == 0 else f"{base}{suffix}"


def extract_device_columns(df: pd.DataFrame):
    """
    Pure column discovery (no mutation)
    """
    tag_cols = [c for c in df.columns if c.startswith("Device Tag")]
    loc_cols = [c for c in df.columns if "Location of Device" in c]
    return tag_cols, loc_cols