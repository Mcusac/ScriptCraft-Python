"""Explicit scalar normalization contracts for asset tools."""

from enum import Enum

import pandas as pd


class TagNormalizationMode(str, Enum):
    """Named modes preserve divergent legacy semantics during staged migration."""

    RECONCILIATION_STRUCTURAL = "reconciliation_structural"
    UPDATER_PEOPLESOFT_SEARCH = "updater_peoplesoft_search"


_RECONCILIATION_NULL_STRINGS = frozenset({"", "nan", "none", "na"})


def is_null(value) -> bool:
    """True null detection across pandas and Python."""
    return value is None or pd.isna(value)


def is_text_null_reconciliation(value) -> bool:
    """Reconciliation null-like strings (empty collapse to '')."""
    if value is None:
        return True

    if is_null(value):
        return True

    if isinstance(value, str):
        return value.strip().lower() in _RECONCILIATION_NULL_STRINGS

    return False


def normalize_null_reconciliation(value) -> str:
    """Canonical null collapse for reconciliation string pipelines."""
    if is_text_null_reconciliation(value):
        return ""

    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.replace(" ", "")


def sanitize_scalar_tag(
    value,
    *,
    mode: TagNormalizationMode = TagNormalizationMode.RECONCILIATION_STRUCTURAL,
) -> str:
    """
    Structural tag cleanup. Business padding rules stay in impl tag_rules.
    """
    if mode != TagNormalizationMode.RECONCILIATION_STRUCTURAL:
        raise ValueError(f"Unsupported tag normalization mode: {mode}")

    return normalize_null_reconciliation(value)


def normalize_updater_tag_digits(
    digits: str,
    *,
    pad_width: int = 8,
) -> str:
    """PeopleSoft search tag formatting used by asset updater."""
    if len(digits) == 6 and digits[0] == "3":
        return digits

    if len(digits) >= pad_width:
        return digits

    return digits.zfill(pad_width)


def normalize_scalar_employee_id(
    raw: str,
    *,
    digits_only: bool = True,
) -> str:
    """
    Strip pandas float artifacts; optionally keep digits only (updater default).
    """
    text = str(raw).strip()

    if text.endswith(".0"):
        text = text[:-2]

    if not digits_only:
        return text

    digits = "".join(character for character in text if character.isdigit())
    return digits if digits else text
