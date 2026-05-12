# ============================================================
# merge_key_preparer.py — schema-safe merge key normalization
#
# DESIGN:
# - Explicit column names only (no positional access)
# - Normalizes each merge key exactly once
# - Casts to string dtype before normalization
# - Filters null/empty keys at DAG boundary
# ============================================================

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_1.contracts import (
    ASSET_REQUIRED_COLUMNS,
    FORM_REQUIRED_COLUMNS,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_3.key_normalizer import (
    normalize_merge_key,
)


def prepare_merge_keys(
    asset_df: pd.DataFrame,
    form_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    DAG stage: normalize merge keys using explicit column names.

    Guarantees:
    - No positional column access
    - Each key column cast to string dtype before normalization
    - Each key normalized exactly once
    - Rows with null/empty keys dropped at this boundary
    """

    asset_df = asset_df.copy()
    form_df = form_df.copy()

    # Explicit contract-driven column names (never positional)
    asset_key = ASSET_REQUIRED_COLUMNS[0]   # "tag"
    form_key = FORM_REQUIRED_COLUMNS[0]     # "tag"

    # Cast to string dtype first to prevent dtype mismatch on assignment.
    # CSV ingestion may infer int64 for numeric-looking tags/IDs;
    # normalize_merge_key returns pandas StringDtype and the assignment
    # would crash without this cast.
    asset_df[asset_key] = asset_df[asset_key].astype("string")
    form_df[form_key] = form_df[form_key].astype("string")

    # Normalize exactly once per key
    asset_df[asset_key] = normalize_merge_key(asset_df[asset_key])
    form_df[form_key] = normalize_merge_key(form_df[form_key])

    # Drop rows whose merge key is null or empty after normalization
    asset_df = asset_df[asset_df[asset_key].notna()].reset_index(drop=True)
    form_df = form_df[form_df[form_key].notna()].reset_index(drop=True)

    return asset_df, form_df