import pandas as pd

from typing import List

from layers.layer_1_tools.level_1_impl.level_0.schema_detector.type_inference import TypeInferenceEngine
from layers.layer_1_tools.level_1_impl.level_0.schema_detector.privacy_classifier import PrivacyClassifier
from layers.layer_1_tools.level_1_impl.level_0.schema_detector.models import ColumnInfo


class ColumnAnalyzer:
    def __init__(self, config, type_engine: TypeInferenceEngine, privacy: PrivacyClassifier):
        self.config = config
        self.type_engine = type_engine
        self.privacy = privacy

    def analyze(self, df: pd.DataFrame, col_name: str) -> ColumnInfo:
        series = df[col_name]

        nullable = series.count() < len(series)
        unique_count = series.nunique()

        sample_values = self._sample(series)

        data_type, sql_type, max_length = self.type_engine.infer(series, col_name)
        privacy_level, pattern, constraints, indexes = self.privacy.classify(col_name)

        return ColumnInfo(
            name=col_name,
            original_name=col_name,
            data_type=data_type,
            sql_type=sql_type,
            nullable=nullable,
            max_length=max_length,
            unique_values=unique_count,
            sample_values=sample_values,
            pattern=pattern,
            constraints=constraints,
            is_primary_key=False,
            is_foreign_key=False,
            suggested_indexes=indexes,
            privacy_level=privacy_level,
        )

    def _sample(self, series: pd.Series, max_samples: int = 3) -> List[str]:
        if not self.config["privacy_mode"]:
            return series.dropna().head(max_samples).astype(str).tolist()

        return ["<masked>"] * min(max_samples, len(series.dropna()))