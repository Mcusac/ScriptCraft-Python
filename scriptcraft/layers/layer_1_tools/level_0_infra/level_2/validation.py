"""
scripts/common/input_validation.py

🔎 Input Validation Utilities.

Handles validation and resolution of input files, ensuring correct file counts 
and formats before proceeding with data processing or comparisons.
"""
import pandas as pd

from pathlib import Path
from typing import Union, Tuple, List, Any, Optional
from dataclasses import dataclass
from abc import abstractmethod

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.plugin_registry import PluginBase


# ==== 🏷️ Validation Result Types ====

@dataclass
class FlaggedValue:
    """Container for flagged validation values."""
    row_index: int
    column: str
    value: Any
    message: str

    @staticmethod
    def from_df_row(df: pd.DataFrame, idx: int, col: str, value: Any, message: str) -> "FlaggedValue":
        return FlaggedValue(
            row_index=idx,
            column=col,
            value=value,
            message=message
        )


# ==== 🔍 Validation Base Classes ====

class ColumnValidator(PluginBase):
    """Base class for all validator plugins."""

    def __init__(self, outlier_method: Optional[Any] = None) -> None:
        super().__init__()
        self.outlier_method = outlier_method

    def get_plugin_type(self) -> str:
        """Return the type of this plugin."""
        return 'validator'

    @abstractmethod
    def validate_value(self, value: Any, expected_values: str) -> Optional[str]:
        """Validate a single value. Return error message if invalid, else None."""
        pass


# Use the unified PluginRegistry from registry.plugin_registry
from ..registry.plugin_registry import PluginRegistry


# ==== 🎨 Validation Utilities ====

# Status indicators with descriptive names for better code readability
STATUS_EMOJI = {
    'success': '✅',  # Operation completed successfully
    'warning': '⚠️',  # Non-critical issue that needs attention
    'error': '❌',    # Critical error that needs immediate attention
    'processing': '🔄', # Operation in progress
    'found_issues': '🔍', # Issues discovered during validation
    'cleaning': '🧹',    # Data cleaning/preprocessing
    'empty': '📭',      # No data to process
    'skipped': '⏭️',    # Operation skipped
    'invalid': '⚠️',    # Invalid data detected
    'valid': '✅',      # Valid data confirmed
    'analyzing': '🔬',  # Detailed analysis in progress
    'completed': '🏁',  # Process completed
}

def get_status_emoji(status: str) -> str:
    """Get emoji for a given status, with fallback"""
    return STATUS_EMOJI.get(status, '❓')


# ==== 📂 Input Validation Functions ====

def validate_input_paths(input_paths: List[Union[str, Path]]) -> List[Path]:
    """
    📂 Validate that exactly two valid input files are provided.

    Args:
        input_paths (List[Union[str, Path]]): List of file paths to validate.

    Returns:
        List[Path]: Validated list of Path objects.

    Raises:
        ValueError: If exactly two paths are not provided.
        FileNotFoundError: If any of the files do not exist.

    Example:
        >>> validated = validate_input_paths(["data/file1.csv", "data/file2.csv"])
        >>> print(validated)
        [PosixPath('data/file1.csv'), PosixPath('data/file2.csv')]
    """
    if len(input_paths) != 2:
        raise ValueError("Exactly two input files must be provided for comparison.")

    paths = [Path(p) for p in input_paths]
    missing_files = [str(p) for p in paths if not p.exists()]

    if missing_files:
        raise FileNotFoundError(f"Missing input files: {', '.join(missing_files)}")

    log_and_print(f"📂 Input files validated: {paths[0]} and {paths[1]}")
    return paths


def auto_resolve_input_files(
    directory: Path, 
    required_count: int = 2, 
    extensions: Tuple[str, ...] = (".csv", ".xlsx", ".xls")
) -> List[Path]:
    """
    🔎 Automatically find the latest files in the provided directory.

    Args:
        directory (Path): Directory to search.
        required_count (int): Number of files to find (default: 2).
        extensions (Tuple[str, ...]): Allowed file extensions.

    Returns:
        List[Path]: List of resolved Path objects for the files.

    Raises:
        FileNotFoundError: If the input directory does not exist.
        ValueError: If the required number of files is not found.

    Example:
        >>> files = auto_resolve_input_files(Path("data/"), required_count=3)
        >>> print(files)
        [PosixPath('data/file1.csv'), PosixPath('data/file2.csv'), PosixPath('data/file3.csv')]
    """
    if not directory.exists():
        raise FileNotFoundError(f"Input directory does not exist: {directory}")

    files = sorted(
        [f for f in directory.glob("*") if f.suffix.lower() in extensions],
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )

    if len(files) < required_count:
        raise ValueError(
            f"Expected {required_count} input files in {directory}, "
            f"but found only {len(files)}."
        )

    selected_files = files[:required_count]
    log_and_print(f"📂 Auto-resolved input files: {', '.join(str(f) for f in selected_files)}")
    return selected_files


def validate_required_columns(df: pd.DataFrame, required_cols: List[str]) -> bool:
    """
    Check if DataFrame has all required columns.
    
    Args:
        df: DataFrame to check
        required_cols: List of required column names
    
    Returns:
        True if all required columns present, False otherwise
    """
    missing = set(required_cols) - set(df.columns)
    if missing:
        log_and_print(f"❌ Missing required columns: {missing}", level="error")
        return False
    return True