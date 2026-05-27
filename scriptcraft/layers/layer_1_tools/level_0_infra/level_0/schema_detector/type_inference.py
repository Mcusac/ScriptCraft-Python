import pandas as pd

from typing import Optional, Tuple


class TypeInferenceEngine:
    def __init__(self, config, data_type_mapping):
        self.config = config
        self.data_type_mapping = data_type_mapping

    def infer(self, series: pd.Series, col_name: str) -> Tuple[str, str, Optional[int]]:
        clean_series = series.dropna()

        if clean_series.empty:
            return "string", self._map("string"), None

        if pd.api.types.is_integer_dtype(clean_series):
            return "integer", self._map("integer"), None

        if pd.api.types.is_float_dtype(clean_series):
            return "float", self._map("float"), None

        if pd.api.types.is_bool_dtype(clean_series):
            return "boolean", self._map("boolean"), None

        if pd.api.types.is_datetime64_any_dtype(clean_series):
            return "datetime", self._map("datetime"), None

        max_length = clean_series.astype(str).str.len().max()
        return "string", self._string_sql(max_length), int(max_length)

    def _map(self, key: str) -> str:
        return self.data_type_mapping[self.config["target_database"]][key]

    def _string_sql(self, max_length: int) -> str:
        db = self.config["target_database"]

        if db == "sqlserver":
            return f"NVARCHAR({min(max_length * 2, 4000)})" if max_length <= 255 else "NVARCHAR(MAX)"
        if db == "postgresql":
            return f"VARCHAR({max_length * 2})" if max_length <= 255 else "TEXT"

        return "TEXT"