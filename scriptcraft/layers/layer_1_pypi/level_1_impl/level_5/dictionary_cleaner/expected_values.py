"""Pure row-level normalizer for the dictionary `Expected Values` column."""

from typing import Any

from layers.layer_1_pypi.level_0_infra.level_1.cleaning import is_missing_like


def _normalize_numeric_range(values: str) -> str:
    if "-" not in values:
        return values
    try:
        min_val, max_val = map(float, values.split("-"))
    except (ValueError, TypeError):
        return values
    return f"{min_val}-{max_val}"


def _normalize_categorical_list(values: str) -> str:
    items = [v.strip() for v in values.split(",")]
    return ", ".join(sorted(set(items)))


def _normalize_date_range(values: str) -> str:
    if "-" not in values:
        return values
    try:
        start, end = map(str.strip, values.split("-"))
    except (ValueError, TypeError):
        return values
    return f"{start} - {end}"


def clean_expected_values(row: Any) -> str:
    """
    Normalize the `Expected Values` cell of a dictionary row based on its `Value Type`.

    Missing-like values are passed through unchanged so that downstream consumers
    can preserve the original sentinel.
    """
    raw = row["Expected Values"]
    if is_missing_like(raw):
        return raw

    val_type = row["Value Type"]
    values = str(raw).strip()

    if val_type == "numeric":
        return _normalize_numeric_range(values)
    if val_type == "categorical":
        return _normalize_categorical_list(values)
    if val_type == "date":
        return _normalize_date_range(values)
    return values
