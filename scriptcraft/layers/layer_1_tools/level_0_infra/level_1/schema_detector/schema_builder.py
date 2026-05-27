from typing import List

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import ColumnInfo, TableSchema


class SchemaBuilder:
    def build(self, name: str, columns: List[ColumnInfo], df) -> TableSchema:
        primary_keys = [c.name for c in columns if c.is_primary_key]

        indexes = []
        for col in columns:
            for idx in col.suggested_indexes:
                indexes.append({"name": col.name, "type": idx, "columns": [col.name]})

        return TableSchema(
            name=name,
            columns=columns,
            primary_keys=primary_keys,
            foreign_keys={},
            indexes=indexes,
            constraints=[],
            estimated_rows=len(df),
            table_type="dimension",
        )