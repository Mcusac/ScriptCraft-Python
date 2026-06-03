"""Validator plugins for dictionary value types beyond simple row checks."""

import re

import pandas as pd

from typing import Any, Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import register_validator
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import ColumnValidator


@register_validator("pattern")
class PatternValidator(ColumnValidator):
    """Validates values against regex patterns."""

    def validate_value(self, value: Any, expected_values: str) -> Optional[str]:
        if pd.isna(value):
            return None

        try:
            pattern = re.compile(expected_values)
            if not pattern.match(str(value)):
                return f"Does not match pattern: {expected_values}"
        except re.error:
            return None

        return None


@register_validator("categorical_multi")
class MultiCategoricalValidator(ColumnValidator):
    """Validates multi-select categorical values."""

    def validate_value(self, value: Any, expected_values: str) -> Optional[str]:
        if pd.isna(value):
            return None

        value_parts = str(value).split(";")
        if len(value_parts) == 1:
            value_parts = str(value).split(",")

        value_parts = [v.strip() for v in value_parts]
        valid_values = [v.strip() for v in expected_values.split(",")]

        invalid_values = [v for v in value_parts if v and v not in valid_values]
        if invalid_values:
            return f"Invalid choices: {', '.join(invalid_values)}"

        return None


@register_validator("coded")
class CodedValueValidator(ColumnValidator):
    """Validates coded values like ICD codes."""

    def validate_value(self, value: Any, expected_values: str) -> Optional[str]:
        if pd.isna(value):
            return None

        try:
            code_type, pattern = expected_values.split(":", 1)
            code_type = code_type.strip()
            pattern = pattern.strip()

            if not re.match(pattern, str(value)):
                return f"Invalid {code_type} code format"

        except ValueError:
            return None

        return None


@register_validator("calculated")
class CalculatedFieldValidator(ColumnValidator):
    """Validates calculated fields against expected formulas."""

    def validate_value(self, value: Any, expected_values: str) -> Optional[str]:
        if pd.isna(value):
            return None

        try:
            formula_match = re.match(r"(\w+)\(([\w,]+)\)", expected_values)
            if not formula_match:
                return None

            operation = formula_match.group(1).lower()
            if operation not in ["sum", "mean", "min", "max"]:
                return f"Unsupported operation: {operation}"

        except Exception:
            return None

        return None
