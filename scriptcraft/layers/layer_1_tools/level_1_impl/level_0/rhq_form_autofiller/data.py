from __future__ import annotations

from pathlib import Path

import pandas as pd

from layers.layer_1_pypi.level_0_infra.level_1.data_loading import load_data

from .constants import AGE_PERIOD_HEADER, AGE_PERIOD_TO_PANEL_INDEX, BLOCK_COLUMNS


def build_address_data(filepath: Path, med_id_filter: str | None = None) -> dict:
    if not filepath.exists():
        raise FileNotFoundError(f"❌ Input file not found: {filepath}")

    df = load_data(filepath)
    if df.empty:
        raise ValueError(f"❌ Excel file is empty: {filepath}")

    if df.index.name == "Med_ID":
        df = df.reset_index()
    elif "Med_ID" not in df.columns:
        raise ValueError("Med_ID not found in data")

    age_period_cols = get_age_period_suffixes(df)

    data: dict = {}
    for _, row in df.iterrows():
        med_id = row["Med_ID"]
        if med_id_filter and str(med_id) != str(med_id_filter):
            continue

        normalized_row = _normalize_block_columns(row)
        panels_data = build_panels_data(normalized_row, age_period_cols)
        data[med_id] = panels_data

    return data


def get_age_period_suffixes(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if col.startswith("AgePeriod")]


def build_panels_data(row, age_period_cols: list[str]) -> list[list[dict]]:
    panels_data: list[list[dict]] = [[] for _ in range(11)]
    for age_col in age_period_cols:
        suffix = "" if age_col == AGE_PERIOD_HEADER else age_col.replace(AGE_PERIOD_HEADER, "")
        age_period = str(row.get(age_col, "")).strip()
        if not age_period:
            continue

        panel_idx = get_panel_index(age_period)
        block_data = {col: row.get(f"{col}{suffix}", "") for col in BLOCK_COLUMNS}
        if is_real_address(block_data):
            panels_data[panel_idx].append(block_data)

    return panels_data


def get_panel_index(age_period: str) -> int:
    return AGE_PERIOD_TO_PANEL_INDEX.get(age_period, 0)


def is_real_address(block_data: dict) -> bool:
    for v in block_data.values():
        if pd.notna(v) and str(v).strip() != "" and str(v).strip().upper() != "MISSING":
            return True
    return False


def _normalize_block_columns(row) -> dict:
    """
    Normalize numeric values in BLOCK_COLUMNS across expected suffixes into clean strings.

    Notes:
      - Keeps behavior consistent with legacy utils: floats that are integer-like become int strings.
      - Converts NaN to empty string.
    """
    normalized = dict(row)
    for col in BLOCK_COLUMNS:
        for suffix in [""] + [f".{i}" for i in range(1, 11)]:
            key = f"{col}{suffix}"
            if key not in normalized:
                continue
            val = normalized[key]
            if pd.isna(val):
                normalized[key] = ""
            elif isinstance(val, float):
                normalized[key] = str(int(val)) if val.is_integer() else str(val)
    return normalized

