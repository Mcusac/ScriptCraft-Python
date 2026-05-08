import pandas as pd

_NULL_STRINGS = {"", "nan", "none", "na"}


def is_null(value) -> bool:
    """
    True null detection across pandas + python + strings.
    """
    return value is None or pd.isna(value)


def is_text_null(value) -> bool:
    """
    Null-like strings (domain-level null semantics).
    """
    if is_null(value):
        return True

    if isinstance(value, str):
        return value.strip().lower() in _NULL_STRINGS

    return False


def normalize_null(value) -> str:
    """
    Canonical null collapse for string pipelines.
    Always returns "" for null-like inputs.
    """
    return "" if is_text_null(value) else value