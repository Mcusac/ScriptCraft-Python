# dictionary_driven_checker/plugins/date_plugin.py
import pandas as pd

from typing import List, Optional, Set, Tuple

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_pypi.level_0_infra.level_0.paths import MISSING_VALUE_STRINGS
from layers.layer_1_pypi.level_0_infra.level_2.validation import FlaggedValue, ColumnValidator, get_status_emoji
from layers.layer_1_pypi.level_0_infra.level_5.config import load_config

from layers.layer_1_pypi.level_1_impl.level_0.dictionary_driven_checker_plugins.registry import register

# Load configuration
config = load_config()
date_config = config.checkers.dictionary_checker.date_validation

class DateValidationError(Exception):
    """Custom exception for date validation errors"""
    pass

@registry.register("date")
class DateValidator(ColumnValidator):
    """Plugin for date validation including format checking"""

    def __init__(self, expected_format: Optional[str] = None):
        """Initialize with expected date format"""
        self.expected_format = expected_format or date_config.get('expected_format', '%m/%Y')

    def validate(self, df: pd.DataFrame, col: str, _: Optional[Set[Tuple[float, float]]] = None) -> List[FlaggedValue]:
        """Validates dates by checking format compliance"""
        flagged = []
        
        try:
            if col not in df.columns:
                log_and_print(f"{get_status_emoji('warning')} Column '{col}' not found in dataframe")
                return flagged

            log_and_print(f"{get_status_emoji('processing')} Validating dates in '{col}'...")

            # Convert to string and handle missing values in a vectorized way
            series = df[col].astype(str)
            mask = ~series.isin(MISSING_VALUE_STRINGS)
            series = series[mask]
            
            if series.empty:
                log_and_print(f"{get_status_emoji('empty')} No date values to validate in '{col}'")
                return flagged

            # Try to convert to datetime using vectorized operation
            log_and_print(f"{get_status_emoji('analyzing')} Checking date format compliance in '{col}'...")
            
            try:
                pd.to_datetime(series, format=self.expected_format)
                log_and_print(f"{get_status_emoji('valid')} All dates in '{col}' match expected format")
            except ValueError:
                # If conversion fails, identify which rows have invalid format
                invalid_dates = pd.Series(True, index=series.index)
                try:
                    parsed_dates = pd.to_datetime(series, format=self.expected_format, errors='coerce')
                    invalid_dates = pd.isna(parsed_dates)
                except Exception as e:
                    log_and_print(f"{get_status_emoji('error')} Error parsing dates: {str(e)}")
                
                invalid_indices = series[invalid_dates].index
                for idx in invalid_indices:
                    flagged.append(
                        FlaggedValue.from_df_row(
                            df, idx, col,
                            df.loc[idx, col],
                            f"{get_status_emoji('invalid')} Invalid date format (expected: {self.expected_format})"
                        )
                    )

            if flagged:
                log_and_print(f"{get_status_emoji('found_issues')} Found {len(flagged)} date format mismatches in '{col}'")

        except Exception as e:
            log_and_print(f"{get_status_emoji('error')} Error validating date column '{col}': {str(e)}")
            
        return flagged

