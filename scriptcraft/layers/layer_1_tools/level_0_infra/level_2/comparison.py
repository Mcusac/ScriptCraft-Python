"""
scripts/common/comparison_utils.py

📏 Utilities for comparing pandas DataFrames, including column checks, 
data type mismatches, content differences, and ID integrity validation.
"""

import pandas as pd

from dataclasses import dataclass
from typing import Set, Tuple, Dict, Union, Optional, List, Any, Callable
from pathlib import Path
from functools import wraps

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.paths import ID_COLUMNS, OUTPUT_DIR


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

def handle_comparison_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_and_print(f"❌ Error in {func.__name__}: {type(e).__name__}: {e}")
            return None
    return wrapper


# ==== 📊 DataFrame Comparer Class ====

class DataFrameComparer:

    def __init__(
        self,
        df1: Union[pd.DataFrame, Set[Any]],
        df2: Union[pd.DataFrame, Set[Any]],
        dataset_name: str = "Dataset",
        output_dir: Union[str, Path] = OUTPUT_DIR
    ) -> None:
        self.df1 = df1
        self.df2 = df2
        self.dataset_name = dataset_name
        self.output_dir = Path(output_dir)
        self._align_dataframes()

    def _align_dataframes(self) -> None:
        if not (isinstance(self.df1, pd.DataFrame) and isinstance(self.df2, pd.DataFrame)):
            return

        if all(col in self.df1.columns and col in self.df2.columns for col in ID_COLUMNS):
            self.df1 = self.df1.set_index(ID_COLUMNS)
            self.df2 = self.df2.set_index(ID_COLUMNS)
            log_and_print(f"🔑 Set composite index on {ID_COLUMNS} for both datasets.")

        self.df1 = self.df1.sort_index()
        self.df2 = self.df2.sort_index()

    # ==== Column Comparison ====

    @handle_comparison_errors
    def compare_columns(self) -> ComparisonResult:
        cols_a = set(self.df1.columns) if isinstance(self.df1, pd.DataFrame) else set(self.df1)
        cols_b = set(self.df2.columns) if isinstance(self.df2, pd.DataFrame) else set(self.df2)

        common = cols_a & cols_b
        only_a = cols_a - cols_b
        only_b = cols_b - cols_a

        self._log_column_comparison(common, only_a, only_b)

        return ComparisonResult(
            common=common,
            only_in_first=only_a,
            only_in_second=only_b,
        )

    def _log_column_comparison(self, common: Set[str], only_a: Set[str], only_b: Set[str]) -> None:
        log_and_print(f"\n🔍 Column Comparison for {self.dataset_name}")
        log_and_print(f"✅ Common Columns: {len(common)}")
        if only_a:
            log_and_print(f"❌ Only in first ({len(only_a)}): {only_a}")
        if only_b:
            log_and_print(f"❌ Only in second ({len(only_b)}): {only_b}")

    # ==== Dtypes ====

    @handle_comparison_errors
    def compare_dtypes(self) -> Dict[str, Tuple[Any, Any]]:
        if not (isinstance(self.df1, pd.DataFrame) and isinstance(self.df2, pd.DataFrame)):
            return {}

        common_cols = set(self.df1.columns) & set(self.df2.columns)

        mismatches = {
            col: (self.df1[col].dtype, self.df2[col].dtype)
            for col in common_cols
            if self.df1[col].dtype != self.df2[col].dtype
        }

        return mismatches

    # ==== Content ====

    @handle_comparison_errors
    def compare_content(self) -> Optional[pd.DataFrame]:
        if not (isinstance(self.df1, pd.DataFrame) and isinstance(self.df2, pd.DataFrame)):
            return None

        common_cols = self.df1.columns.intersection(self.df2.columns)
        differences = self.df1[common_cols].compare(self.df2[common_cols])

        if differences.empty:
            log_and_print("✅ No content differences found.")
            return None

        self.output_dir.mkdir(exist_ok=True)
        path = self.output_dir / f"{self.dataset_name}_content_differences.csv"
        differences.to_csv(path)

        return differences

    # ==== Shapes ====

    @handle_comparison_errors
    def compare_shapes(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        if not (isinstance(self.df1, pd.DataFrame) and isinstance(self.df2, pd.DataFrame)):
            return None

        if self.df1.shape == self.df2.shape:
            return None

        return self.df1.shape, self.df2.shape

    # ==== Index ====

    @handle_comparison_errors
    def compare_indexes(self) -> Optional[Tuple[Set[Any], Set[Any], Set[Any]]]:
        if not (isinstance(self.df1, pd.DataFrame) and isinstance(self.df2, pd.DataFrame)):
            return None

        idx_old = set(self.df1.index)
        idx_new = set(self.df2.index)

        return idx_old & idx_new, idx_old - idx_new, idx_new - idx_old

    # ==== Full Run ====

    def run_full_comparison(self, steps: Optional[List[str]] = None) -> ComparisonResult:
        steps = steps or ["columns", "dtypes", "shape", "index", "rows", "med_ids"]

        column_results = (
            self.compare_columns()
            if "columns" in steps
            else ComparisonResult(common=set(), only_in_first=set(), only_in_second=set())
        )

        return ComparisonResult(
            common=column_results.common,
            only_in_first=column_results.only_in_first,
            only_in_second=column_results.only_in_second,
            differences=self.compare_content() if "rows" in steps else None,
            dtype_mismatches=self.compare_dtypes() if "dtypes" in steps else {},
            shape_mismatch=self.compare_shapes() if "shape" in steps else None,
            index_comparison=self.compare_indexes() if "index" in steps else None,
            missing_ids=self.compare_med_visit_ids() if "med_ids" in steps else None,
        )


# ==== Convenience API ====

def compare_dataframes(
    df1,
    df2,
    dataset_name: str = "Dataset",
    output_dir: Union[str, Path] = OUTPUT_DIR,
    steps: Optional[List[str]] = None,
) -> ComparisonResult:
    comparer = DataFrameComparer(df1, df2, dataset_name, output_dir)
    return comparer.run_full_comparison(steps)