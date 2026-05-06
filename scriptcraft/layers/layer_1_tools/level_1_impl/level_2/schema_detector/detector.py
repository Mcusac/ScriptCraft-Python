from pathlib import Path
from typing import List

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.directory_ops import ensure_output_dir
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.version import __version__
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7.base_tool import BaseTool

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.schema_detector.data_loader import DataLoader
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.schema_detector.type_inference import TypeInferenceEngine
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.schema_detector.privacy_classifier import PrivacyClassifier
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.schema_detector.models import TableSchema
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1.schema_detector.column_analyzer import ColumnAnalyzer
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1.schema_detector.schema_builder import SchemaBuilder
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1.schema_detector.outputs import save_outputs


class SchemaDetector(BaseTool):
    def __init__(self):
        super().__init__(name="schema_detector", description="🔍 Schema detection tool")

        self.config = {
            "sample_size": 1000,
            "privacy_mode": True,
            "target_database": "sqlite",
            "output_formats": ["sql", "json", "yaml"],
        }

        self.data_type_mapping = {
            "sqlite": {"integer": "INTEGER", "float": "REAL", "string": "TEXT"}
        }

        self.healthcare_patterns = {}

        # compose services
        self.loader = DataLoader(self.config["sample_size"])
        self.type_engine = TypeInferenceEngine(self.config, self.data_type_mapping)
        self.privacy = PrivacyClassifier(self.healthcare_patterns)
        self.column_analyzer = ColumnAnalyzer(self.config, self.type_engine, self.privacy)
        self.builder = SchemaBuilder()

    def run(self, input_paths: List[str], output_dir: str = "output", **kwargs):
        self.log_start()

        output_path = ensure_output_dir(output_dir)

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