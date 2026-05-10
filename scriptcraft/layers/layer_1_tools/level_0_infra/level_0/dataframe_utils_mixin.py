import pandas as pd

from typing import Any, Dict, List, Optional


class DataFrameUtilsMixin:
    """Handles DataFrame utilities."""

    def shallow_compare_dataframes(
        self,
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        compare_columns: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        comparison = {
            'shape_difference': df1.shape != df2.shape,
            'df1_shape': df1.shape,
            'df2_shape': df2.shape,
            'column_differences': set(df1.columns) ^ set(df2.columns),
            'common_columns': set(df1.columns) & set(df2.columns),
        }

        if compare_columns:
            comparison['column_differences'] = (
                set(compare_columns) ^ set(df1.columns) ^ set(df2.columns)
            )

        return comparison