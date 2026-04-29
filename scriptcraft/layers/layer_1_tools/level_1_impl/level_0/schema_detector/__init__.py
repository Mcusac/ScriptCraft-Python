"""Schema detector package (DRY, cohesive modules)."""

from .models import ColumnInfo, TableSchema
from .detector import SchemaDetector

__all__ = [
    "ColumnInfo",
    "TableSchema",
    "SchemaDetector",
]

