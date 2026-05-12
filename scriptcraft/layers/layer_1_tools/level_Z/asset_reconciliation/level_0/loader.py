# ============================================================
# loader.py — CSV input layer
#
# DESIGN:
# - dtype=str at load time prevents pandas from inferring
#   int64 for numeric-looking columns (tags, IDs, locations).
# - Downstream normalization stages receive consistent object
#   strings and are responsible for casting to pandas StringDtype.
# ============================================================

import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV with all columns read as Python str.

    Rationale: tags, employee IDs, and asset IDs are identifiers,
    not numbers. Allowing pandas to infer int64 for values like
    "37435" causes dtype crashes when string normalization results
    are assigned back to those columns.
    """
    return pd.read_csv(path, dtype=str)