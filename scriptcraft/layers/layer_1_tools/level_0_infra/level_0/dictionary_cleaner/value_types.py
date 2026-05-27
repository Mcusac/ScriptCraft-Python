"""Value-type vocabulary used to normalize dictionary `Value Type` cells."""

from typing import Mapping

VALUE_TYPE_MAP: Mapping[str, str] = {
    "numeric": "numeric",
    "number": "numeric",
    "float": "numeric",
    "int": "numeric",
    "integer": "numeric",
    "categorical": "categorical",
    "category": "categorical",
    "text": "text",
    "string": "text",
    "date": "date",
    "datetime": "date",
    "timestamp": "date",
}

_DEFAULT_VALUE_TYPE = "text"


def normalize_value_type(value: str) -> str:
    """Map an arbitrary value-type label to the canonical vocabulary."""
    if not isinstance(value, str):
        return _DEFAULT_VALUE_TYPE
    return VALUE_TYPE_MAP.get(value.strip().lower(), _DEFAULT_VALUE_TYPE)
