"""
scripts/common/date_utils.py

📅 Utilities for detecting, parsing, and standardizing date values 
within pandas DataFrames. Supports multiple output formats, 
including ISO strings, datetime objects, and plain dates.
"""
import pandas as pd

from enum import Enum
from typing import Any, Optional, Union, List, Dict
from dateutil.parser import parse

# ==== 📚 Configuration & Constants ====

class DateOutputType(Enum):
    """Enum representing supported standardized date output types."""
    
    DATE = "date"
    DATETIME = "datetime"
    ISO_STRING = "iso_string"

DEFAULT_SAMPLE_SIZE: int = 10
DEFAULT_DATE_FORMAT: str = "%Y-%m-%d"
MIN_SAMPLE_SIZE: int = 1

DATE_FORMATS: Dict[str, str] = {
    "iso": "%Y-%m-%d",
    "us": "%m/%d/%Y",
    "eu": "%d/%m/%Y",
    "datetime": "%Y-%m-%d %H:%M:%S"
}

# ==== 📅 Date Detection Utilities ====

def is_date_column(series: pd.Series, sample_size: int = DEFAULT_SAMPLE_SIZE) -> bool:
    """
    Detect if a column likely contains date-like values using a sample of the data.

    Args:
        series: Column to check.
        sample_size: Number of non-null values to sample for detection.

    Returns:
        True if column is likely a date column, False otherwise.
    """
    if sample_size < MIN_SAMPLE_SIZE:
        raise ValueError(f"Sample size must be at least {MIN_SAMPLE_SIZE}")

    non_null_values = series.dropna().astype(str).head(sample_size)
    if non_null_values.empty:
        return False

    parsed_count = sum(1 for val in non_null_values if try_parse_date(val))
    result = parsed_count >= max(MIN_SAMPLE_SIZE, sample_size // 2)
    return result


def try_parse_date(value: str) -> bool:
    """
    Helper function to safely attempt date parsing.

    Args:
        value: String value to attempt parsing.

    Returns:
        True if successfully parsed as a date, False otherwise.
    """
    try:
        parse(value, fuzzy=False)
        return True
    except (ValueError, TypeError):
        return False


def matches_date_format(value: Any, fmt: str) -> bool:
    """Return True when ``value`` parses with the given datetime format."""
    try:
        pd.to_datetime(str(value).strip(), format=fmt)
        return True
    except (ValueError, TypeError):
        return False


def coerce_datetime_with_format(series: pd.Series, fmt: str) -> pd.Series:
    """Coerce to datetime with a specified format (invalid rows -> NaT)."""
    return pd.to_datetime(series, format=fmt, errors="coerce")

# ==== 📏 Date Standardization Utilities ====

def standardize_date_column(
    series: pd.Series,
    output_type: Union[DateOutputType, str] = DateOutputType.DATE,
    date_format: Optional[str] = None
) -> pd.Series:
    """
    Convert a Series to a standardized date or datetime format.

    Args:
        series: Column to convert.
        output_type: Desired output type (DateOutputType enum or string).
        date_format: Optional custom format string for ISO_STRING output.

    Returns:
        Converted Series with standardized date formats.
    """
    try:
        if isinstance(output_type, str):
            output_type = DateOutputType(output_type.lower())

        parsed_series = pd.to_datetime(series, errors="coerce")

        if output_type == DateOutputType.DATETIME:
            return parsed_series
        elif output_type == DateOutputType.ISO_STRING:
            format_str = date_format or DATE_FORMATS["iso"]
            return parsed_series.dt.strftime(format_str)
        else:  # Default: DateOutputType.DATE
            return parsed_series.dt.date

    except Exception as e:
        _ = e
        return series


def standardize_dates_in_dataframe(
    df: pd.DataFrame,
    columns_to_check: Optional[List[str]] = None,
    output_type: Union[DateOutputType, str] = DateOutputType.DATE,
    date_format: Optional[str] = None,
    sample_size: int = DEFAULT_SAMPLE_SIZE
) -> pd.DataFrame:
    """
    Standardize date columns in a DataFrame to a specified format.

    Args:
        df: Input DataFrame.
        columns_to_check: Subset of columns to evaluate. Defaults to all columns.
        output_type: Desired output type (DateOutputType enum or string).
        date_format: Optional format string for ISO_STRING outputs.
        sample_size: Sample size for detecting date columns.

    Returns:
        DataFrame with standardized date columns.
    """
    standardized = df.copy()
    columns = columns_to_check or df.columns

    for col in columns:
        if is_date_column(df[col], sample_size=sample_size):
            standardized[col] = standardize_date_column(
                df[col],
                output_type=output_type,
                date_format=date_format
            )

    return standardized
