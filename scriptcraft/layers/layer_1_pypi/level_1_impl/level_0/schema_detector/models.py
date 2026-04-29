from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ColumnInfo:
    """📊 Information about a dataset column"""

    name: str
    original_name: str
    data_type: str
    sql_type: str
    nullable: bool
    max_length: Optional[int]
    unique_values: int
    sample_values: List[str]
    pattern: Optional[str]
    constraints: List[str]
    is_primary_key: bool
    is_foreign_key: bool
    suggested_indexes: List[str]
    privacy_level: str  # 'public', 'internal', 'sensitive', 'highly_sensitive'


@dataclass
class TableSchema:
    """🏗️ Complete table schema information"""

    name: str
    columns: List[ColumnInfo]
    primary_keys: List[str]
    foreign_keys: Dict[str, str]
    indexes: List[Dict[str, Any]]
    constraints: List[str]
    estimated_rows: int
    table_type: str  # 'fact', 'dimension', 'lookup', 'audit'

