import pandas as pd

from typing import Any, Optional, Set


from layers.layer_1_pypi.level_0_infra.level_1.expected_values import extract_expected_values


def validate_against_dictionary(
    value: Any,
    expected_values: Optional[str],
    value_type: str,
    column: str,
) -> Optional[str]:
    """Core dictionary validation logic. Returns an error message if invalid, else None."""
    _ = column  # reserved for more contextual messages

    if pd.isna(value):
        return None

    if not expected_values:
        return None

    value_type = str(value_type).lower().strip()

    if value_type == "categorical":
        valid_values = _extract_categorical_values(expected_values)
        if str(value).strip() not in valid_values:
            return "Not in dictionary"

    elif value_type == "numeric":
        try:
            numeric_value = float(value)
            if "-" in expected_values:
                min_val, max_val = map(float, expected_values.split("-"))
                if not (min_val <= numeric_value <= max_val):
                    return f"Outside valid range: {expected_values}"
            elif any(op in expected_values for op in [">", "<", "="]):
                # NOTE: This preserves legacy behavior; can be replaced with a safer parser later.
                if not eval(f"{numeric_value} {expected_values}"):
                    return f"Does not satisfy: {expected_values}"
        except ValueError:
            return "Non-numeric value"

    return None


def _extract_categorical_values(expected_values: str) -> Set[str]:
    """
    Normalize expected-values parsing to a set[str] for categorical checks.

    `extract_expected_values()` returns `(value_type, parsed_values)` where `parsed_values`
    can be a set, a list of ranges, or a mixed tuple depending on dictionary content.
    """
    _value_type, parsed = extract_expected_values(expected_values)

    if isinstance(parsed, set):
        return {str(x).strip() for x in parsed}

    if isinstance(parsed, tuple) and len(parsed) == 2:
        maybe_set, _maybe_ranges = parsed
        if isinstance(maybe_set, set):
            return {str(x).strip() for x in maybe_set}

    return set()

