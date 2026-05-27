"""Infra row-value helpers for asset updater datasets."""

from typing import Any
from typing import Iterable
from typing import Literal

import pandas as pd

from scriptcraft.layers.layer_0_core.level_1 import is_missing_like

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    normalize_scalar_employee_id,
    normalize_updater_tag_digits,
)

UpdateKind = Literal["both", "location_only", "custodian_only"]


def is_present(value: Any) -> bool:
    """
    True when value is a meaningful non-null field value.
    """
    if value is None:
        return False

    if isinstance(value, float) and pd.isna(value):
        return False

    text = str(value).strip()

    if not text:
        return False

    if text.lower() == "nan":
        return False

    _ = is_missing_like(value)

    return True


def optional_value_from_row(
    row: dict[str, Any],
    keys: Iterable[str],
) -> str | None:
    for key in keys:
        value = row.get(key)
        if is_present(value):
            return str(value).strip()
    return None


def value_from_row(
    row: dict[str, Any],
    keys: Iterable[str],
    label: str,
) -> str:
    value = optional_value_from_row(row, keys)
    if value is not None:
        return value

    raise KeyError(
        f"Row missing {label}. Expected one of: {tuple(keys)}"
    )


def normalize_tag_number(
    digits: str,
    *,
    pad_width: int = 8,
) -> str:
    return normalize_updater_tag_digits(digits, pad_width=pad_width)


def tag_number_from_row(
    row: dict[str, Any],
    tag_keys: Iterable[str],
    *,
    pad_width: int = 8,
) -> str:
    raw = value_from_row(row, tag_keys, "tag identifier")

    if raw.endswith(".0"):
        raw = raw[:-2]

    digits = "".join(character for character in raw if character.isdigit())

    if digits:
        return normalize_tag_number(digits, pad_width=pad_width)

    return raw.zfill(pad_width)


def normalize_employee_id(raw: str) -> str:
    return normalize_scalar_employee_id(raw, digits_only=True)


def optional_location_code_from_row(
    row: dict[str, Any],
    location_keys: Iterable[str],
) -> str | None:
    return optional_value_from_row(row, location_keys)


def optional_employee_id_from_row(
    row: dict[str, Any],
    employee_keys: Iterable[str],
) -> str | None:
    raw = optional_value_from_row(row, employee_keys)
    if raw is None:
        return None
    return normalize_employee_id(raw)


def location_code_from_row(
    row: dict[str, Any],
    location_keys: Iterable[str],
) -> str:
    return value_from_row(row, location_keys, "location code")


def employee_id_from_row(
    row: dict[str, Any],
    employee_keys: Iterable[str],
) -> str:
    raw = value_from_row(row, employee_keys, "employee id")
    return normalize_employee_id(raw)


def classify_update_row(
    row: dict[str, Any],
    *,
    location_keys: Iterable[str],
    employee_keys: Iterable[str],
) -> UpdateKind:
    has_location = optional_location_code_from_row(row, location_keys) is not None
    has_custodian = optional_employee_id_from_row(row, employee_keys) is not None

    if has_location and has_custodian:
        return "both"

    if has_location:
        return "location_only"

    return "custodian_only"
