import pandas as pd


def project_columns_required(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Schema-strict projection that requires all requested columns.
    """
    return (
        df[columns]
        .reset_index(drop=True)
    )


def project_columns_available(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Safe projection that keeps only columns that exist.
    """
    available = [c for c in columns if c in df.columns]
    return df[available].copy()
