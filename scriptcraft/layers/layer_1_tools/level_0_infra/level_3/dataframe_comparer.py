"""
DataFrame comparison orchestration (workspace alignment, logging, artifacts).
"""

from pathlib import Path
from typing import Any, List, Optional, Sequence, Set, Union

import pandas as pd

from scriptcraft.layers.layer_0_core.level_0 import (
    ComparisonResult,
    column_sets,
    content_differences,
    dtype_mismatches,
    index_sets,
    shape_mismatch,
)

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    WorkspaceConfig,
    log_and_print,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import handle_comparison_errors


class DataFrameComparer:

    def __init__(
        self,
        df1: Union[pd.DataFrame, Set[Any]],
        df2: Union[pd.DataFrame, Set[Any]],
        dataset_name: str = "Dataset",
        output_dir: Optional[Union[str, Path]] = None,
        id_columns: Optional[Sequence[str]] = None,
    ) -> None:
        self.df1 = df1
        self.df2 = df2
        self.dataset_name = dataset_name
        self.id_columns: Sequence[str] = (
            tuple(id_columns)
            if id_columns is not None
            else tuple(WorkspaceConfig().id_columns)
        )
        self.output_dir = (
            Path(output_dir)
            if output_dir is not None
            else Path("output")
        )
        self._align_dataframes()

    def _align_dataframes(self) -> None:
        if not (
            isinstance(self.df1, pd.DataFrame)
            and isinstance(self.df2, pd.DataFrame)
        ):
            return

        if all(
            col in self.df1.columns and col in self.df2.columns
            for col in self.id_columns
        ):
            self.df1 = self.df1.set_index(list(self.id_columns))
            self.df2 = self.df2.set_index(list(self.id_columns))
            log_and_print(
                f"🔑 Set composite index on {list(self.id_columns)} for both datasets."
            )

        self.df1 = self.df1.sort_index()
        self.df2 = self.df2.sort_index()

    @handle_comparison_errors
    def compare_dataframe_columns(self) -> ComparisonResult:
        common, only_a, only_b = column_sets(self.df1, self.df2)
        self._log_column_comparison(common=common, only_a=only_a, only_b=only_b)
        return ComparisonResult(
            common=common,
            only_in_first=only_a,
            only_in_second=only_b,
        )

    def _log_column_comparison(
        self,
        common: Set[str],
        only_a: Set[str],
        only_b: Set[str],
    ) -> None:
        log_and_print(f"\n🔍 Column Comparison for {self.dataset_name}")
        log_and_print(f"✅ Common Columns: {len(common)}")
        if only_a:
            log_and_print(f"❌ Only in first ({len(only_a)}): {only_a}")
        if only_b:
            log_and_print(f"❌ Only in second ({len(only_b)}): {only_b}")

    @handle_comparison_errors
    def compare_dtypes(self) -> dict:
        if not (
            isinstance(self.df1, pd.DataFrame)
            and isinstance(self.df2, pd.DataFrame)
        ):
            return {}

        mismatches = dtype_mismatches(self.df1, self.df2)
        if mismatches:
            log_and_print(f"⚠️ Found {len(mismatches)} dtype mismatches.")
        return mismatches

    @handle_comparison_errors
    def compare_content(self) -> Optional[pd.DataFrame]:
        if not (
            isinstance(self.df1, pd.DataFrame)
            and isinstance(self.df2, pd.DataFrame)
        ):
            return None

        differences = content_differences(self.df1, self.df2)
        if differences is None:
            log_and_print("✅ No content differences found.")
            return None

        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = (
            self.output_dir / f"{self.dataset_name}_content_differences.csv"
        )
        differences.to_csv(output_path)
        log_and_print(f"📝 Saved content differences to: {output_path}")
        return differences

    @handle_comparison_errors
    def compare_shapes(
        self,
    ) -> Optional[tuple[tuple[int, int], tuple[int, int]]]:
        if not (
            isinstance(self.df1, pd.DataFrame)
            and isinstance(self.df2, pd.DataFrame)
        ):
            return None
        return shape_mismatch(self.df1, self.df2)

    @handle_comparison_errors
    def compare_indexes(
        self,
    ) -> Optional[tuple[Set[Any], Set[Any], Set[Any]]]:
        if not (
            isinstance(self.df1, pd.DataFrame)
            and isinstance(self.df2, pd.DataFrame)
        ):
            return None
        return index_sets(self.df1, self.df2)

    def run_full_comparison(
        self,
        steps: Optional[List[str]] = None,
    ) -> ComparisonResult:
        steps = steps or [
            "columns",
            "dtypes",
            "shape",
            "index",
            "rows",
        ]

        column_results = (
            self.compare_dataframe_columns()
            if "columns" in steps
            else ComparisonResult(
                common=set(),
                only_in_first=set(),
                only_in_second=set(),
            )
        )

        return ComparisonResult(
            common=column_results.common,
            only_in_first=column_results.only_in_first,
            only_in_second=column_results.only_in_second,
            differences=(
                self.compare_content()
                if "rows" in steps
                else None
            ),
            dtype_mismatches=(
                self.compare_dtypes()
                if "dtypes" in steps
                else {}
            ),
            shape_mismatch=(
                self.compare_shapes()
                if "shape" in steps
                else None
            ),
            index_comparison=(
                self.compare_indexes()
                if "index" in steps
                else None
            ),
        )


def compare_dataframes(
    df1: Union[pd.DataFrame, Set[Any]],
    df2: Union[pd.DataFrame, Set[Any]],
    dataset_name: str = "Dataset",
    output_dir: Optional[Union[str, Path]] = None,
    steps: Optional[List[str]] = None,
    id_columns: Optional[Sequence[str]] = None,
) -> ComparisonResult:
    comparer = DataFrameComparer(
        df1=df1,
        df2=df2,
        dataset_name=dataset_name,
        output_dir=output_dir,
        id_columns=id_columns,
    )
    return comparer.run_full_comparison(steps=steps)
