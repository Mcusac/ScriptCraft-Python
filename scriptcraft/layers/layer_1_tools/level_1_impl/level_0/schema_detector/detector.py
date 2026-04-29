from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from layers.layer_1_pypi.level_0_infra.level_0._version import __version__
from layers.layer_1_pypi.level_0_infra.level_0.directory_ops import ensure_output_dir
from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print, setup_logger
from layers.layer_1_pypi.level_0_infra.level_6.base_tool import BaseTool

from .models import ColumnInfo, TableSchema
from .outputs import save_outputs


class SchemaDetector(BaseTool):
    """🔍 Schema detection tool for datasets"""

    def __init__(self):
        super().__init__(name="schema_detector", description="🔍 Analyzes datasets and generates database schemas")

        self.config = {
            "sample_size": 1000,
            "privacy_mode": True,
            "target_database": "sqlite",
            "generate_indexes": True,
            "suggest_constraints": True,
            "output_formats": ["sql", "json", "yaml"],
            "healthcare_mode": True,
            "naming_convention": "pascal_case",
        }

        self.supported_formats = {".csv", ".xlsx", ".xls", ".json", ".parquet"}
        self.healthcare_patterns = self._init_healthcare_patterns()
        self.data_type_mapping = self._init_data_type_mapping()

        self.logger = setup_logger(self.name)

    def run(
        self,
        input_paths: List[str],
        output_dir: str = "output",
        target_database: str = None,
        privacy_mode: bool = None,
        **kwargs,
    ):
        self.log_start()

        if target_database:
            self.config["target_database"] = target_database
        if privacy_mode is not None:
            self.config["privacy_mode"] = privacy_mode

        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value

        log_and_print("🔍 Starting schema detection analysis...")
        log_and_print(f"📂 Files to analyze: {len(input_paths)}")
        log_and_print(f"🎯 Target database: {self.config['target_database']}")
        log_and_print(f"🔐 Privacy mode: {'Enabled' if self.config['privacy_mode'] else 'Disabled'}")

        output_path = ensure_output_dir(output_dir)
        schemas = self.analyze_datasets(input_paths)

        if not schemas:
            log_and_print("❌ No schemas could be detected from the provided files", level="error")
            return False

        log_and_print(f"✅ Successfully analyzed {len(schemas)} schema(s)")

        for schema in schemas:
            log_and_print(f"  🗂️ {schema.name}: {len(schema.columns)} columns, {schema.table_type} table")
            privacy_counts: Dict[str, int] = {}
            for col in schema.columns:
                privacy_counts[col.privacy_level] = privacy_counts.get(col.privacy_level, 0) + 1
            if privacy_counts:
                privacy_summary = ", ".join([f"{count} {level}" for level, count in privacy_counts.items()])
                log_and_print(f"    🔐 Privacy levels: {privacy_summary}")

        sql_content = self.generate_sql_schema(schemas)
        save_outputs(
            schemas,
            output_path,
            output_formats=self.config["output_formats"],
            tool_version=__version__,
            target_database=self.config["target_database"],
            sql_content=sql_content,
        )

        log_and_print("🎉 Schema detection completed successfully!")
        log_and_print(f"📁 Results saved to: {output_path}")
        return True

    def analyze_datasets(self, input_paths: List[str]) -> List[TableSchema]:
        schemas: List[TableSchema] = []
        log_and_print(f"📂 Analyzing {len(input_paths)} dataset(s)")

        for path in input_paths:
            path_obj = Path(path)

            if not path_obj.exists():
                log_and_print(f"⚠️ File not found: {path}", level="warning")
                continue

            if path_obj.suffix.lower() not in self.supported_formats:
                log_and_print(f"⚠️ Unsupported format: {path_obj.suffix}", level="warning")
                continue

            try:
                schema = self._analyze_single_dataset(path_obj)
                if schema:
                    schemas.append(schema)
                    log_and_print(f"✅ Successfully analyzed: {path_obj.name}")
            except Exception as e:
                log_and_print(f"❌ Error analyzing {path_obj.name}: {str(e)}", level="error")

        return schemas

    def _init_healthcare_patterns(self) -> Dict[str, Dict]:
        return {
            "patient_id": {
                "patterns": [r"patient[_\s]*id", r"med[_\s]*id", r"mrn", r"medical[_\s]*record"],
                "sql_type": "TEXT",
                "constraints": ["UNIQUE", "NOT NULL"],
                "privacy": "sensitive",
                "indexes": ["PRIMARY KEY"],
            },
            "ssn": {
                "patterns": [r"ssn", r"social[_\s]*security", r"tax[_\s]*id"],
                "sql_type": "TEXT",
                "constraints": ["UNIQUE"],
                "privacy": "highly_sensitive",
                "indexes": ["UNIQUE"],
            },
            "date_of_birth": {
                "patterns": [r"dob", r"birth[_\s]*date", r"date[_\s]*of[_\s]*birth"],
                "sql_type": "DATE",
                "constraints": ["NOT NULL"],
                "privacy": "sensitive",
                "indexes": [],
            },
            "diagnosis": {
                "patterns": [r"diagnosis", r"icd[_\s]*code", r"condition"],
                "sql_type": "TEXT",
                "constraints": [],
                "privacy": "highly_sensitive",
                "indexes": ["INDEX"],
            },
            "lab_value": {
                "patterns": [r"lab[_\s]*result", r"test[_\s]*value", r"result"],
                "sql_type": "REAL",
                "constraints": [],
                "privacy": "sensitive",
                "indexes": [],
            },
        }

    def _init_data_type_mapping(self) -> Dict[str, Dict[str, str]]:
        return {
            "sqlite": {
                "integer": "INTEGER",
                "float": "REAL",
                "string": "TEXT",
                "date": "TEXT",
                "datetime": "TEXT",
                "boolean": "INTEGER",
                "json": "TEXT",
            },
            "sqlserver": {
                "integer": "INT",
                "float": "DECIMAL(18,2)",
                "string": "NVARCHAR",
                "date": "DATE",
                "datetime": "DATETIME2",
                "boolean": "BIT",
                "json": "NVARCHAR(MAX)",
            },
            "postgresql": {
                "integer": "INTEGER",
                "float": "DECIMAL(10,2)",
                "string": "VARCHAR",
                "date": "DATE",
                "datetime": "TIMESTAMP",
                "boolean": "BOOLEAN",
                "json": "JSONB",
            },
        }

    def _analyze_single_dataset(self, file_path: Path) -> Optional[TableSchema]:
        log_and_print(f"🔍 Analyzing {file_path.name}...")
        df = self._load_data_sample(file_path)
        if df is None or df.empty:
            return None

        table_name = self._generate_table_name(file_path.stem)

        columns: List[ColumnInfo] = []
        for col_name in df.columns:
            columns.append(self._analyze_column(df, col_name))

        primary_keys = self._identify_primary_keys(columns, df)
        foreign_keys = self._identify_foreign_keys(columns)

        indexes = self._generate_indexes(columns, primary_keys)
        constraints = self._generate_constraints(columns)

        table_type = self._classify_table_type(table_name, columns)

        return TableSchema(
            name=table_name,
            columns=columns,
            primary_keys=primary_keys,
            foreign_keys=foreign_keys,
            indexes=indexes,
            constraints=constraints,
            estimated_rows=len(df) if len(df) <= self.config["sample_size"] else -1,
            table_type=table_type,
        )

    def _load_data_sample(self, file_path: Path) -> Optional[pd.DataFrame]:
        try:
            sample_size = self.config["sample_size"]

            if file_path.suffix.lower() == ".csv":
                df = pd.read_csv(file_path, nrows=sample_size)
                log_and_print(f"📋 Found {len(df.columns)} columns in CSV")
                return df

            if file_path.suffix.lower() in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path, nrows=sample_size)
                log_and_print(f"📋 Found {len(df.columns)} columns in Excel")
                return df

            if file_path.suffix.lower() == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    df = pd.DataFrame(data[:sample_size])
                else:
                    df = pd.DataFrame([data])
                log_and_print(f"📋 Found {len(df.columns)} columns in JSON")
                return df

            if file_path.suffix.lower() == ".parquet":
                df = pd.read_parquet(file_path, nrows=sample_size)
                log_and_print(f"📋 Found {len(df.columns)} columns in Parquet")
                return df

            log_and_print(f"❌ Unsupported file format: {file_path.suffix}", level="error")
            return None

        except Exception as e:
            log_and_print(f"❌ Error reading {file_path.name}: {str(e)}", level="error")
            return None

    # ---- Column analysis & inference (kept as methods for now) ----
    def _analyze_column(self, df: pd.DataFrame, col_name: str) -> ColumnInfo:
        series = df[col_name]
        non_null_count = series.count()
        total_count = len(series)
        unique_count = series.nunique()
        nullable = non_null_count < total_count

        sample_values = self._get_safe_sample_values(series)
        data_type, sql_type, max_length = self._infer_data_type(series, col_name)
        privacy_level, pattern, constraints, indexes = self._check_healthcare_patterns(col_name)
        constraints.extend(self._analyze_constraints(series, data_type))

        is_primary_key = self._could_be_primary_key(series, col_name)
        is_foreign_key = self._could_be_foreign_key(col_name)
        clean_name = self._clean_column_name(col_name)

        return ColumnInfo(
            name=clean_name,
            original_name=col_name,
            data_type=data_type,
            sql_type=sql_type,
            nullable=nullable,
            max_length=max_length,
            unique_values=unique_count,
            sample_values=sample_values,
            pattern=pattern,
            constraints=constraints,
            is_primary_key=is_primary_key,
            is_foreign_key=is_foreign_key,
            suggested_indexes=indexes,
            privacy_level=privacy_level,
        )

    def _get_safe_sample_values(self, series: pd.Series, max_samples: int = 3) -> List[str]:
        if not self.config["privacy_mode"]:
            return series.dropna().head(max_samples).astype(str).tolist()

        samples: List[str] = []
        for value in series.dropna().head(max_samples):
            if pd.api.types.is_numeric_dtype(type(value)):
                samples.append("<numeric_value>")
            elif isinstance(value, str):
                if len(value) <= 3:
                    samples.append("<short_text>")
                elif len(value) <= 10:
                    samples.append("<medium_text>")
                else:
                    samples.append("<long_text>")
            else:
                samples.append(f"<{type(value).__name__}>")
        return samples

    def _infer_data_type(self, series: pd.Series, col_name: str) -> Tuple[str, str, Optional[int]]:
        clean_series = series.dropna()
        if clean_series.empty:
            return "string", self.data_type_mapping[self.config["target_database"]]["string"], None

        if pd.api.types.is_integer_dtype(clean_series):
            return "integer", self.data_type_mapping[self.config["target_database"]]["integer"], None
        if pd.api.types.is_float_dtype(clean_series):
            return "float", self.data_type_mapping[self.config["target_database"]]["float"], None
        if pd.api.types.is_bool_dtype(clean_series):
            return "boolean", self.data_type_mapping[self.config["target_database"]]["boolean"], None
        if pd.api.types.is_datetime64_any_dtype(clean_series):
            return "datetime", self.data_type_mapping[self.config["target_database"]]["datetime"], None

        if self._could_be_date(clean_series):
            return "date", self.data_type_mapping[self.config["target_database"]]["date"], None

        if self._could_be_numeric(clean_series):
            if self._could_be_integer(clean_series):
                return "integer", self.data_type_mapping[self.config["target_database"]]["integer"], None
            return "float", self.data_type_mapping[self.config["target_database"]]["float"], None

        max_length = clean_series.astype(str).str.len().max() if not clean_series.empty else 50

        if self.config["target_database"] == "sqlserver":
            if max_length <= 255:
                sql_type = f"NVARCHAR({min(max_length * 2, 4000)})"
            else:
                sql_type = "NVARCHAR(MAX)"
        elif self.config["target_database"] == "postgresql":
            if max_length <= 255:
                sql_type = f"VARCHAR({max_length * 2})"
            else:
                sql_type = "TEXT"
        else:
            sql_type = "TEXT"

        _ = col_name
        return "string", sql_type, int(max_length) if max_length is not None else None

    def _could_be_date(self, series: pd.Series) -> bool:
        if len(series) == 0:
            return False
        sample = series.head(min(10, len(series)))
        date_count = 0
        for value in sample:
            try:
                pd.to_datetime(value)
                date_count += 1
            except Exception:
                continue
        return date_count / len(sample) > 0.5

    def _could_be_numeric(self, series: pd.Series) -> bool:
        if len(series) == 0:
            return False
        sample = series.head(min(10, len(series)))
        numeric_count = 0
        for value in sample:
            try:
                float(str(value))
                numeric_count += 1
            except Exception:
                continue
        return numeric_count / len(sample) > 0.8

    def _could_be_integer(self, series: pd.Series) -> bool:
        if len(series) == 0:
            return False
        sample = series.head(min(10, len(series)))
        for value in sample:
            try:
                float_val = float(str(value))
                if float_val != int(float_val):
                    return False
            except Exception:
                return False
        return True

    def _check_healthcare_patterns(self, col_name: str) -> Tuple[str, Optional[str], List[str], List[str]]:
        col_lower = col_name.lower().replace("_", " ").replace("-", " ")
        for pattern_name, pattern_info in self.healthcare_patterns.items():
            for pattern in pattern_info["patterns"]:
                if re.search(pattern, col_lower, re.IGNORECASE):
                    return (
                        pattern_info["privacy"],
                        pattern_name,
                        pattern_info["constraints"].copy(),
                        pattern_info["indexes"].copy(),
                    )
        if any(term in col_lower for term in ["id", "key", "number"]):
            return "internal", None, [], ["INDEX"]
        if any(term in col_lower for term in ["name", "address", "phone", "email"]):
            return "sensitive", None, [], []
        return "public", None, [], []

    def _analyze_constraints(self, series: pd.Series, data_type: str) -> List[str]:
        constraints: List[str] = []
        if series.count() == len(series):
            constraints.append("NOT NULL")
        if series.nunique() == series.count():
            constraints.append("UNIQUE")
        if data_type in ["integer", "float"]:
            min_val = series.min()
            if min_val >= 0:
                constraints.append(f"CHECK ({self._clean_column_name(series.name)} >= 0)")
        return constraints

    def _could_be_primary_key(self, series: pd.Series, col_name: str) -> bool:
        col_lower = col_name.lower()
        if any(pattern in col_lower for pattern in ["id", "key", "number"]) and col_lower.endswith("id"):
            if series.nunique() == series.count() and series.count() == len(series):
                return True
        return False

    def _could_be_foreign_key(self, col_name: str) -> bool:
        col_lower = col_name.lower()
        fk_patterns = ["patient_id", "provider_id", "user_id", "visit_id", "appointment_id"]
        return any(pattern in col_lower for pattern in fk_patterns)

    def _clean_column_name(self, col_name: str) -> str:
        clean_name = re.sub(r"[^\w\s]", "", col_name)
        if self.config["naming_convention"] == "snake_case":
            clean_name = re.sub(r"\s+", "_", clean_name.lower())
        elif self.config["naming_convention"] == "pascal_case":
            clean_name = "".join(word.capitalize() for word in clean_name.split())
        elif self.config["naming_convention"] == "camel_case":
            words = clean_name.split()
            clean_name = words[0].lower() + "".join(word.capitalize() for word in words[1:]) if words else ""
        return clean_name

    def _generate_table_name(self, filename: str) -> str:
        name = re.sub(r"(_data|_dataset|_table|_export)", "", filename.lower())
        if self.config["naming_convention"] == "pascal_case":
            name = "".join(word.capitalize() for word in name.split("_"))
        return name

    # ---- The remaining methods are left intact in the original module for the next pass. ----
    # For this first split, we keep SQL generation and relationship logic minimal/stable.

    def _identify_primary_keys(self, columns: List[ColumnInfo], df: pd.DataFrame) -> List[str]:
        primary_keys = [col.name for col in columns if col.is_primary_key]
        if not primary_keys:
            for col in columns:
                if "id" in col.name.lower() and "UNIQUE" in col.constraints:
                    primary_keys.append(col.name)
                    break
        _ = df
        return primary_keys

    def _identify_foreign_keys(self, columns: List[ColumnInfo]) -> Dict[str, str]:
        foreign_keys: Dict[str, str] = {}
        for col in columns:
            if col.is_foreign_key:
                foreign_keys[col.name] = col.name.replace("_id", "")
        return foreign_keys

    def _generate_indexes(self, columns: List[ColumnInfo], primary_keys: List[str]) -> List[Dict[str, Any]]:
        indexes: List[Dict[str, Any]] = []
        for col in columns:
            if col.name in primary_keys:
                indexes.append({"name": col.name, "type": "PRIMARY KEY", "columns": [col.name]})
            for idx_type in col.suggested_indexes:
                if idx_type == "PRIMARY KEY":
                    continue
                indexes.append({"name": col.name, "type": idx_type, "columns": [col.name]})
        return indexes

    def _generate_constraints(self, columns: List[ColumnInfo]) -> List[str]:
        constraints: List[str] = []
        for col in columns:
            for c in col.constraints:
                if c.startswith("CHECK"):
                    constraints.append(c)
        return constraints

    def _classify_table_type(self, table_name: str, columns: List[ColumnInfo]) -> str:
        name_lower = table_name.lower()
        if any(term in name_lower for term in ["lookup", "ref", "code"]):
            return "lookup"
        if any(term in name_lower for term in ["audit", "log", "history"]):
            return "audit"
        if any(col.is_foreign_key for col in columns):
            return "fact"
        return "dimension"

    def generate_sql_schema(self, schemas: List[TableSchema]) -> str:
        parts: List[str] = []
        for schema in schemas:
            parts.append(self._generate_table_sql(schema))
            parts.append(self._generate_indexes_sql(schema))
            parts.append("")
        return "\n".join(parts).strip()

    def _generate_table_sql(self, schema: TableSchema) -> str:
        lines = [f"CREATE TABLE {schema.name} ("]
        column_lines: List[str] = []
        for col in schema.columns:
            column_lines.append(self._format_column_definition(col))
        if schema.primary_keys:
            pk_cols = ", ".join(schema.primary_keys)
            column_lines.append(f"    PRIMARY KEY ({pk_cols})")
        for constraint in schema.constraints:
            column_lines.append(f"    {constraint}")
        lines.append(",\n".join(column_lines))
        lines.append(");")
        return "\n".join(lines)

    def _format_column_definition(self, col: ColumnInfo) -> str:
        parts = [col.name, col.sql_type]
        for constraint in col.constraints:
            if constraint not in ["PRIMARY KEY", "UNIQUE"]:
                parts.append(constraint)
        definition = " ".join(parts) + ","
        if col.original_name != col.name or col.privacy_level != "public":
            comment_parts: List[str] = []
            if col.original_name != col.name:
                comment_parts.append(f"Originally: {col.original_name}")
            if col.privacy_level != "public":
                comment_parts.append(f"Privacy: {col.privacy_level}")
            definition += f"  -- {', '.join(comment_parts)}"
        return definition

    def _generate_indexes_sql(self, schema: TableSchema) -> str:
        lines: List[str] = []
        for index in schema.indexes:
            if index["type"] == "PRIMARY KEY":
                continue
            index_name = f"{index['name']}_{schema.name}"
            columns = ", ".join(index["columns"])
            if index["type"] == "UNIQUE":
                lines.append(f"CREATE UNIQUE INDEX {index_name} ON {schema.name} ({columns});")
            else:
                lines.append(f"CREATE INDEX {index_name} ON {schema.name} ({columns});")
        return "\n".join(lines)

