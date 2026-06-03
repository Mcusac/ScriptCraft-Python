from pathlib import Path
from typing import List

from scriptcraft._version import __version__

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    PrivacyClassifier,
    TableSchema,
    TypeInferenceEngine,
    log_and_print,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    ColumnAnalyzer,
    DataLoader,
    SchemaBuilder,
    save_outputs,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import ArgumentValidator


class SchemaDetector:
    """Domain engine composing infra schema-detection services."""

    def __init__(self) -> None:
        self.config = {
            "sample_size": 1000,
            "privacy_mode": True,
            "target_database": "sqlite",
            "output_formats": ["sql", "json", "yaml"],
        }

        self.data_type_mapping = {
            "sqlite": {"integer": "INTEGER", "float": "REAL", "string": "TEXT"}
        }

        self.healthcare_patterns: dict = {}

        self.loader = DataLoader(self.config["sample_size"])
        self.type_engine = TypeInferenceEngine(self.config, self.data_type_mapping)
        self.privacy = PrivacyClassifier(self.healthcare_patterns)
        self.column_analyzer = ColumnAnalyzer(
            self.config, self.type_engine, self.privacy
        )
        self.builder = SchemaBuilder()

    def run(self, input_paths: List[str], output_dir: str = "output", **kwargs) -> bool:
        log_and_print("🔍 Starting schema detection...")

        output_path = ArgumentValidator.ensure_output_dir(output_dir)

        schemas: List[TableSchema] = []

        for path in input_paths:
            df = self.loader.load(Path(path))
            if df is None:
                continue

            columns = [self.column_analyzer.analyze(df, col) for col in df.columns]
            schema = self.builder.build(Path(path).stem, columns, df)

            schemas.append(schema)

        if not schemas:
            log_and_print("❌ No schemas detected", level="error")
            return False

        save_outputs(
            schemas,
            output_path,
            output_formats=self.config["output_formats"],
            tool_version=__version__,
            target_database=self.config["target_database"],
            sql_content="",
        )

        return True
