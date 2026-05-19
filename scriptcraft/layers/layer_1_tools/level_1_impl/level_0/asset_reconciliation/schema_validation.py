import pandas as pd


def require_columns(
    df: pd.DataFrame,
    required: list[str],
    context: str = "",
) -> None:
    """
    Ensures required columns exist.
    """
    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise RuntimeError(
            f"[SCHEMA ERROR] Missing columns in "
            f"{context}: {missing}"
        )
