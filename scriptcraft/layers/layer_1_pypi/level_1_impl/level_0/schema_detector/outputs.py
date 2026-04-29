from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print

from .models import ColumnInfo, TableSchema


def schema_to_dict(schema: TableSchema) -> Dict[str, Any]:
    """🔄 Convert TableSchema to dictionary for JSON/YAML export"""
    return {
        "name": schema.name,
        "type": schema.table_type,
        "estimated_rows": schema.estimated_rows,
        "columns": [
            {
                "name": col.name,
                "original_name": col.original_name,
                "data_type": col.data_type,
                "sql_type": col.sql_type,
                "nullable": bool(col.nullable),
                "max_length": col.max_length,
                "unique_values": int(col.unique_values) if col.unique_values is not None else None,
                "privacy_level": col.privacy_level,
                "constraints": col.constraints,
                "is_primary_key": bool(col.is_primary_key),
                "is_foreign_key": bool(col.is_foreign_key),
                "sample_values": col.sample_values,
            }
            for col in schema.columns
        ],
        "primary_keys": schema.primary_keys,
        "foreign_keys": schema.foreign_keys,
        "indexes": schema.indexes,
        "constraints": schema.constraints,
    }


def generate_documentation(
    schemas: List[TableSchema],
    *,
    tool_version: str,
    target_database: str,
) -> str:
    """📚 Generate documentation for the detected schema."""
    doc_parts: List[str] = []

    doc_parts.append(
        f"""
# 📊 Dataset Schema Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Tool**: Schema Detection Tool v{tool_version}  
**Database Target**: {target_database.upper()}  
**Tables Analyzed**: {len(schemas)}

## 🔍 Analysis Summary

| Metric | Value |
|--------|-------|
| Total Tables | {len(schemas)} |
| Total Columns | {sum(len(s.columns) for s in schemas)} |
| Primary Keys Detected | {sum(1 for s in schemas if s.primary_keys)} |
| Foreign Keys Detected | {sum(len(s.foreign_keys) for s in schemas)} |
| Highly Sensitive Columns | {sum(1 for s in schemas for c in s.columns if c.privacy_level == 'highly_sensitive')} |
| Sensitive Columns | {sum(1 for s in schemas for c in s.columns if c.privacy_level == 'sensitive')} |
"""
    )

    doc_parts.append("## 🏗️ Table Schemas\n")

    for schema in schemas:
        doc_parts.append(f"### {schema.name}\n")
        doc_parts.append(f"**Type**: {schema.table_type.title()}")
        if schema.estimated_rows > 0:
            doc_parts.append(f"  \n**Estimated Rows**: {schema.estimated_rows:,}")
        doc_parts.append("\n")

        doc_parts.append("| Column | Type | Nullable | Privacy | Constraints |")
        doc_parts.append("|--------|------|----------|---------|-------------|")

        for col in schema.columns:
            nullable = "✅" if col.nullable else "❌"
            privacy_emoji = {
                "public": "🟢",
                "internal": "🟡",
                "sensitive": "🟠",
                "highly_sensitive": "🔴",
            }.get(col.privacy_level, "⚪")

            constraints = ", ".join(col.constraints) if col.constraints else "-"

            doc_parts.append(
                f"| {col.name} | {col.data_type} | {nullable} | {privacy_emoji} {col.privacy_level} | {constraints} |"
            )

        doc_parts.append("\n")

    doc_parts.append("## 🔐 Privacy & Security Recommendations\n")

    for schema in schemas:
        sensitive_cols = [c for c in schema.columns if c.privacy_level in ["sensitive", "highly_sensitive"]]
        if sensitive_cols:
            doc_parts.append(f"### {schema.name}")
            for col in sensitive_cols:
                if col.privacy_level == "highly_sensitive":
                    doc_parts.append(f"- **{col.name}**: Requires encryption at rest and in transit")
                else:
                    doc_parts.append(f"- **{col.name}**: Requires access logging and controlled access")
            doc_parts.append("")

    return "\n".join(doc_parts)


def save_outputs(
    schemas: List[TableSchema],
    output_dir: Path,
    *,
    output_formats: List[str],
    tool_version: str,
    target_database: str,
    sql_content: str,
) -> None:
    """💾 Save all generated outputs."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if "sql" in output_formats:
        sql_file = output_dir / f"detected_schema_{timestamp}.sql"
        with open(sql_file, "w", encoding="utf-8") as f:
            f.write(sql_content)
        log_and_print(f"💾 SQL schema saved: {sql_file}")

    if "json" in output_formats:
        json_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "tool_version": tool_version,
                "target_database": target_database,
            },
            "schemas": [schema_to_dict(schema) for schema in schemas],
        }
        json_file = output_dir / f"detected_schema_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
        log_and_print(f"💾 JSON schema saved: {json_file}")

    if "yaml" in output_formats:
        yaml_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "tool_version": tool_version,
                "target_database": target_database,
            },
            "schemas": [schema_to_dict(schema) for schema in schemas],
        }
        yaml_file = output_dir / f"detected_schema_{timestamp}.yaml"
        with open(yaml_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
        log_and_print(f"💾 YAML schema saved: {yaml_file}")

    doc_content = generate_documentation(
        schemas,
        tool_version=tool_version,
        target_database=target_database,
    )
    doc_file = output_dir / f"schema_analysis_report_{timestamp}.md"
    with open(doc_file, "w", encoding="utf-8") as f:
        f.write(doc_content)
    log_and_print(f"📚 Documentation saved: {doc_file}")

