import operator
import re
import pandas as pd

from typing import Any, Optional, Set

from scriptcraft.layers.layer_0_core.level_2 import validate_numeric_against_ranges

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import log_and_extract_expected_values

_OPERATOR_PATTERN = re.compile(r"^(>=|<=|>|<|==|=)\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)$")
_OPERATOR_FUNCS = {
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
    "=": operator.eq,
}


def _numeric_satisfies_operator_constraint(value: float, expected_values: str) -> bool:
    match = _OPERATOR_PATTERN.match(expected_values.strip())
    if not match:
        return False
    op_str, bound_str = match.groups()
    bound = float(bound_str)
    return _OPERATOR_FUNCS[op_str](value, bound)


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
        except (TypeError, ValueError):
            return "Non-numeric value"

        err = validate_numeric_against_ranges(value, expected_values)
        if err:
            return err

        if "-" in expected_values and not any(
            op in expected_values for op in (">", "<", "=")
        ):
            try:
                min_val, max_val = map(float, expected_values.split("-", 1))
                if not (min_val <= numeric_value <= max_val):
                    return f"Outside valid range: {expected_values}"
            except ValueError:
                return "Non-numeric value"
        elif any(op in expected_values for op in (">", "<", "=")):
            if not _numeric_satisfies_operator_constraint(
                numeric_value, expected_values
            ):
                return f"Does not satisfy: {expected_values}"

    return None


def _extract_categorical_values(expected_values: str) -> Set[str]:
    """
    Normalize expected-values parsing to a set[str] for categorical checks.

    ``log_and_extract_expected_values()`` returns ``(value_type, parsed_values)``
    where ``parsed_values`` can be a set, a list of ranges, or a mixed tuple.
    """
    _value_type, parsed = log_and_extract_expected_values(expected_values)

    if isinstance(parsed, set):
        return {str(x).strip() for x in parsed}

    if isinstance(parsed, tuple) and len(parsed) == 2:
        maybe_set, _maybe_ranges = parsed
        if isinstance(maybe_set, set):
            return {str(x).strip() for x in maybe_set}

    return set()
