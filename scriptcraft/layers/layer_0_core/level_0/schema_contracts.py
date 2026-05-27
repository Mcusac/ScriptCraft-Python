"""DataFrame schema contract primitives."""

import pandas as pd


def require_columns(
    df: pd.DataFrame,
    required: list[str],
    context: str = "",
) -> None:
    """Ensure all required columns exist (subset contract)."""
    missing = [column for column in required if column not in df.columns]

    if missing:
        raise RuntimeError(
            f"[SCHEMA ERROR] Missing columns in {context}: {missing}"
        )


def require_exact_columns(
    df: pd.DataFrame,
    required: list[str],
    context: str = "",
) -> None:
    """Enforce exact schema contract; prevents silent schema drift."""
    actual = set(df.columns)
    expected = set(required)

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)

    if missing or extra:
        raise RuntimeError(
            f"[SCHEMA VIOLATION] {context}\n"
            f"Missing: {missing}\n"
            f"Unexpected: {extra}"
        )
