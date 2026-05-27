"""
Supplement domain-specific cleaning + schema construction
"""

from typing import Any, Dict, Optional, Union

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    clean_dataframe,
    standardize_columns,
)


def clean_supplement_data(df):
    """
    Supplement-specific cleanup (delegates to canonical cleaner).
    """
    return clean_dataframe(df)


def standardize_supplement_columns(df):
    """
    Normalize supplement schema naming.
    """
    return standardize_columns(df, {
        "variable": "Main Variable",
        "notes": "Label",
        "min": "Min_Value",
        "max": "Max_Value",
    })


def create_standardized_supplement_row(
    variable: str,
    label: str = "",
    min_val: Optional[Union[int, float]] = None,
    max_val: Optional[Union[int, float]] = None,
    missing_unit: str = "-9999",
    quality_level: str = "Supplement",
    visits: str = "",
    notes: str = "",
) -> Dict[str, Any]:
    """
    Create normalized supplement row.
    """
    if min_val is not None and max_val is not None:
        try:
            value = f"{{{int(float(min_val))}-{int(float(max_val))}}}"
        except Exception:
            value = "Numeric"
    else:
        value = "Numeric"

    return {
        "Main Variable": str(variable).strip(),
        "Label": str(label).strip(),
        "Value": value,
        "Missing/Unit of Measure": str(missing_unit),
        "Level of quality check": str(quality_level),
        "Visits": str(visits),
        "Notes": str(notes),
    }