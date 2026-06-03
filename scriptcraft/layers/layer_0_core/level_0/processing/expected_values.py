"""Log-free parsing utilities for dictionary `Expected Values` specifications.

This module is intentionally side-effect free (no logging, no I/O) so it can live in
`layer_0_core` and be reused by tools and plugins.
"""

import re
import pandas as pd

from enum import Enum
from typing import List, Set, Tuple, Union


class ValueType(Enum):
    """Enum representing different parsed value types."""

    NUMERIC = "numeric"
    TEXT = "text"
    DATE = "date"
    RANGE_SET = "range_set"
    SET = "set"
    MIXED_SET = "mixed_set"
    UNKNOWN = "unknown"


RANGE_KEYWORDS: List[str] = ["range"]
VALUE_PATTERNS: dict[str, str] = {
    "range": r"^\d+(\.\d+)?\s*-\s*\d+(\.\d+)?$",
    "set_entry": r"\{(.*?)\}",
}

ParsedExpectedValues = Union[
    Set[str],
    List[Tuple[float, float]],
    Tuple[Set[str], List[Tuple[float, float]]],
]


def parse_expected_values_with_messages(
    value_string: str,
    *,
    strict: bool = False,
) -> Tuple[str, ParsedExpectedValues, List[str]]:
    """Parse a dictionary value string and return value type, parsed values, and diagnostics."""
    return _extract_expected_values_with_messages(value_string, strict=strict)


def extract_expected_values(
    value_string: str,
    *,
    strict: bool = False,
) -> Tuple[str, ParsedExpectedValues]:
    """Parse a dictionary value string into expected types, ranges, or sets (log-free)."""
    value_type, parsed, _messages = parse_expected_values_with_messages(
        value_string, strict=strict
    )
    return value_type, parsed


def extract_expected_values_messages(
    value_string: str,
    *,
    strict: bool = False,
) -> List[str]:
    """Return diagnostic messages from parsing (log-free; no parsed payload)."""
    _value_type, _parsed, messages = parse_expected_values_with_messages(
        value_string, strict=strict
    )
    return messages


def parse_numeric_ranges(
    expected_values: str,
) -> Set[Tuple[float, float]] | None:
    """Parse expected-values text into inclusive numeric ranges (or None)."""
    if pd.isna(expected_values) or not str(expected_values).strip():
        return None

    value_type, parsed = extract_expected_values(str(expected_values))
    if value_type == ValueType.RANGE_SET.value and isinstance(parsed, list):
        return {(float(low), float(high)) for low, high in parsed}

    if value_type == ValueType.MIXED_SET.value and isinstance(parsed, tuple):
        _categorical, ranges = parsed
        if isinstance(ranges, list) and ranges:
            return {(float(low), float(high)) for low, high in ranges}

    return None


def _extract_expected_values_with_messages(
    value_string: str,
    *,
    strict: bool,
) -> Tuple[str, ParsedExpectedValues, List[str]]:
    messages: List[str] = []

    if pd.isna(value_string) or not str(value_string).strip():
        messages.append("⚠️ Empty or null value string")
        return ValueType.UNKNOWN.value, set(), messages

    text = str(value_string).strip()
    lowered = text.lower()

    if lowered == ValueType.NUMERIC.value:
        return ValueType.NUMERIC.value, set(), messages
    if lowered == ValueType.TEXT.value:
        return ValueType.TEXT.value, set(), messages
    if lowered == "mm/yyyy":
        return ValueType.DATE.value, set(), messages

    try:
        matches = re.findall(VALUE_PATTERNS["set_entry"], text)
        if not matches:
            if strict:
                raise ValueError(f"No valid set entries found in: {text}")
            return ValueType.UNKNOWN.value, set(), messages

        parsed: Set[str] = set()
        ranges: List[Tuple[float, float]] = []

        for entry in matches:
            parts = [p.strip() for p in entry.split(",")]
            key_part = parts[0]
            label = parts[1].lower() if len(parts) > 1 else ""

            if any(kw in label for kw in RANGE_KEYWORDS) or re.match(
                VALUE_PATTERNS["range"], key_part
            ):
                try:
                    low, high = map(float, key_part.replace(" ", "").split("-"))
                    ranges.append((low, high))
                    messages.append(f"📊 Parsed range: {low}-{high}")
                except Exception as e:
                    messages.append(f"⚠️ Failed to parse range '{key_part}': {e}")
                    if strict:
                        raise
                    parsed.add(key_part)
            else:
                try:
                    key_numeric = float(key_part)
                    parsed.add(
                        str(int(key_numeric))
                        if key_numeric.is_integer()
                        else str(key_numeric)
                    )
                except ValueError:
                    parsed.add(key_part)

        if ranges and not parsed:
            return ValueType.RANGE_SET.value, ranges, messages
        if parsed and not ranges:
            return ValueType.SET.value, parsed, messages
        return ValueType.MIXED_SET.value, (parsed, ranges), messages

    except Exception as e:
        messages.append(f"❌ Error parsing value string '{text}': {e}")
        if strict:
            raise
        return ValueType.UNKNOWN.value, set(), messages

