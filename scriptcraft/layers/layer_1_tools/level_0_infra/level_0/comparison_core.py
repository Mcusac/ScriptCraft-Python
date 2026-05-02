"""
Core DataFrame comparison: identifies added, removed, modified, and unchanged rows.
"""

import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class DataFrameDiffResult:
    """Result of a row-level DataFrame comparison."""
    added_rows: pd.DataFrame
    removed_rows: pd.DataFrame
    modified_rows: pd.DataFrame
    unchanged_rows: pd.DataFrame
    column_changes: Dict[str, Dict[str, int]]  # col -> {modified: n}
    summary: Dict[str, int]                    # {added, removed, modified, unchanged}


class CoreDataFrameComparer:
    """
    Compares two DataFrames row-by-row using explicit key columns.

    Rows are matched by (key_column, ...) tuples; unmatched rows in
    *new_df* are 'added', unmatched rows in *old_df* are 'removed'.
    """

    def __init__(
        self,
        old_df: pd.DataFrame,
        new_df: pd.DataFrame,
        key_columns: List[str],
        compare_columns: Optional[List[str]] = None,
    ) -> None:
        self.old_df = old_df.copy()
        self.new_df = new_df.copy()
        self.key_columns = key_columns
        self.compare_columns = compare_columns or [
            col for col in old_df.columns if col not in key_columns
        ]

    def compare(self) -> DataFrameDiffResult:
        """
        Perform the comparison and return a DataFrameDiffResult.

        Uses index-based lookup to avoid O(n²) row scanning.
        """
        old_indexed = self.old_df.set_index(self.key_columns)
        new_indexed = self.new_df.set_index(self.key_columns)

        old_keys = set(old_indexed.index.tolist())
        new_keys = set(new_indexed.index.tolist())

        added_keys   = new_keys - old_keys
        removed_keys = old_keys - new_keys
        common_keys  = old_keys & new_keys

        added_rows = (
            new_indexed.loc[list(added_keys)].reset_index()
            if added_keys else self.new_df.iloc[:0]
        )
        removed_rows = (
            old_indexed.loc[list(removed_keys)].reset_index()
            if removed_keys else self.old_df.iloc[:0]
        )

        cols = [
            c for c in self.compare_columns
            if c in old_indexed.columns and c in new_indexed.columns
        ]

        column_changes: Dict[str, Dict[str, int]] = {
            col: {"modified": 0} for col in cols
        }

        modified_rows = []
        unchanged_rows = []

        for key in common_keys:
            old_row = old_indexed.loc[key]
            new_row = new_indexed.loc[key]

            changed = False
            for col in cols:
                if old_row[col] != new_row[col]:
                    column_changes[col]["modified"] += 1
                    changed = True

            (modified_rows if changed else unchanged_rows).append(new_row)

        def _to_df(rows: list) -> pd.DataFrame:
            if not rows:
                return self.new_df.iloc[:0].drop(columns=self.key_columns, errors="ignore")
            return pd.DataFrame(rows).reset_index()

        modified_df = _to_df(modified_rows)
        unchanged_df = _to_df(unchanged_rows)

        return DataFrameDiffResult(
            added_rows=added_rows,
            removed_rows=removed_rows,
            modified_rows=modified_df,
            unchanged_rows=unchanged_df,
            column_changes=column_changes,
            summary={
                "added": len(added_rows),
                "removed": len(removed_rows),
                "modified": len(modified_df),
                "unchanged": len(unchanged_df),
            },
        )