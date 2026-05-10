"""
scripts/common/comparison_utils.py

📏 Utilities for comparing pandas DataFrames, including column checks,
data type mismatches, content differences, and ID integrity validation.
"""

from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

import pandas as pd

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import (
    log_and_print,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.workspace_schema import (
    WorkspaceConfig,
)


# ==== 📦 Comparison Results Data Class ====


@dataclass
class ComparisonResult:
    """
    High-level comparison result across multiple dimensions.
    """

    common: Set[str]
    only_in_first: Set[str]
    only_in_second: Set[str]

    differences: Optional[pd.DataFrame] = None
    dtype_mismatches: Optional[Dict[str, Tuple[Any, Any]]] = None
    shape_mismatch: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
    missing_ids: Optional[Tuple[pd.DataFrame, pd.DataFrame]] = None
    index_comparison: Optional[Tuple[Set[Any], Set[Any], Set[Any]]] = None

    def __post_init__(self) -> None:
        if self.dtype_mismatches is None:
            self.dtype_mismatches = {}


# ==== 🚨 Error Handling Decorator ====


def handle_comparison_errors(
    func: Callable[..., Any],
) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)

        except Exception as exc:
            log_and_print(
                f"❌ Error in {func.__name__}: "
                f"{type(exc).__name__}: {exc}"
            )
            return None

    return wrapper


# ==== 📊 DataFrame Comparer Class ====


class DataFrameComparer:

    def __init__(
        self,
        df1: Union[pd.DataFrame, Set[Any]],
        df2: Union[pd.DataFrame, Set[Any]],
        dataset_name: str = "Dataset",
        output_dir: Optional[Union[str, Path]] = None,
    ) -> None:

        self.df1 = df1
        self.df2 = df2
        self.dataset_name = dataset_name

        # Avoid import-time execution/config dependency issues
        self.output_dir = (
            Path(output_dir)
            if output_dir is not None
            else Path("output")
        )

        self._align_dataframes()

    # ==== Internal Helpers ====

    def _align_dataframes(self) -> None:

        if not (
            isinstance(self.df1, pd.DataFrame)
            and isinstance(self.df2, pd.DataFrame)
        ):
            return

        if all(
            col in self.df1.columns and col in self.df2.columns
            for col in WorkspaceConfig.id_columns
        ):

            self.df1 = self.df1.set_index(
                WorkspaceConfig.id_columns
            )

            self.df2 = self.df2.set_index(
                WorkspaceConfig.id_columns
            )

            log_and_print(
                f"🔑 Set composite index on "
                f"{WorkspaceConfig.id_columns} "
                f"for both datasets."
            )

        self.df1 = self.df1.sort_index()
        self.df2 = self.df2.sort_index()

    # ==== Column Comparison ====

    @handle_comparison_errors
    def compare_columns(self) -> ComparisonResult:

        cols_a = (
            set(self.df1.columns)
            if isinstance(self.df1, pd.DataFrame)
            else set(self.df1)
        )

        cols_b = (
            set(self.df2.columns)
            if isinstance(self.df2, pd.DataFrame)
            else set(self.df2)
        )

        common = cols_a & cols_b
        only_a = cols_a - cols_b
        only_b = cols_b - cols_a

        self._log_column_comparison(
            common=common,
            only_a=only_a,
            only_b=only_b,
        )

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

        log_and_print(
            f"\n🔍 Column Comparison for {self.dataset_name}"
        )

        log_and_print(
            f"✅ Common Columns: {len(common)}"
        )

        if only_a:
            log_and_print(
                f"❌ Only in first ({len(only_a)}): {only_a}"
            )

        if only_b:
            log_and_print(
                f"❌ Only in second ({len(only_b)}): {only_b}"
            )

    # ==== Dtype Comparison ====

    @handle_comparison_errors
    def compare_dtypes(
        self,
    ) -> Dict[str, Tuple[Any, Any]]:

        if not (
            isinstance(self.df1, pd.DataFrame)
            and isinstance(self.df2, pd.DataFrame)
        ):
            return {}

        common_cols = (
            set(self.df1.columns)
            & set(self.df2.columns)
        )

        mismatches = {
            col: (
                self.df1[col].dtype,
                self.df2[col].dtype,
            )
            for col in common_cols
            if self.df1[col].dtype != self.df2[col].dtype
        }

        if mismatches:
            log_and_print(
                f"⚠️ Found {len(mismatches)} dtype mismatches."
            )

        return mismatches

    # ==== Content Comparison ====

    @handle_comparison_errors
    def compare_content(
        self,
    ) -> Optional[pd.DataFrame]:

        if not (
            isinstance(self.df1, pd.DataFrame)
            and isinstance(self.df2, pd.DataFrame)
        ):
            return None

        common_cols = self.df1.columns.intersection(
            self.df2.columns
        )

        differences = self.df1[common_cols].compare(
            self.df2[common_cols]
        )

        if differences.empty:
            log_and_print(
                "✅ No content differences found."
            )
            return None

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            self.output_dir
            / f"{self.dataset_name}_content_differences.csv"
        )

        differences.to_csv(output_path)

        log_and_print(
            f"📝 Saved content differences to: "
            f"{output_path}"
        )

        return differences

    # ==== Shape Comparison ====

    @handle_comparison_errors
    def compare_shapes(
        self,
    ) -> Optional[
        Tuple[Tuple[int, int], Tuple[int, int]]
    ]:

        if not (
            isinstance(self.df1, pd.DataFrame)
            and isinstance(self.df2, pd.DataFrame)
        ):
            return None

        if self.df1.shape == self.df2.shape:
            return None

        return (
            self.df1.shape,
            self.df2.shape,
        )

    # ==== Index Comparison ====

    @handle_comparison_errors
    def compare_indexes(
        self,
    ) -> Optional[
        Tuple[Set[Any], Set[Any], Set[Any]]
    ]:

        if not (
            isinstance(self.df1, pd.DataFrame)
            and isinstance(self.df2, pd.DataFrame)
        ):
            return None

        idx_1 = set(self.df1.index)
        idx_2 = set(self.df2.index)

        common = idx_1 & idx_2
        only_1 = idx_1 - idx_2
        only_2 = idx_2 - idx_1

        return (
            common,
            only_1,
            only_2,
        )

    # ==== Placeholder Compatibility Method ====

    @handle_comparison_errors
    def compare_med_visit_ids(
        self,
    ) -> Optional[
        Tuple[pd.DataFrame, pd.DataFrame]
    ]:
        """
        Placeholder retained for backward compatibility.

        Replace with actual implementation if needed.
        """

        return None

    # ==== Full Comparison Runner ====

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
            "med_ids",
        ]

        column_results = (
            self.compare_columns()
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

            missing_ids=(
                self.compare_med_visit_ids()
                if "med_ids" in steps
                else None
            ),
        )


# ==== Convenience API ====


def compare_dataframes(
    df1: Union[pd.DataFrame, Set[Any]],
    df2: Union[pd.DataFrame, Set[Any]],
    dataset_name: str = "Dataset",
    output_dir: Optional[Union[str, Path]] = None,
    steps: Optional[List[str]] = None,
) -> ComparisonResult:

    comparer = DataFrameComparer(
        df1=df1,
        df2=df2,
        dataset_name=dataset_name,
        output_dir=output_dir,
    )

    return comparer.run_full_comparison(
        steps=steps
    )