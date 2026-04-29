"""Dictionary cleaning utilities split into cohesive modules."""

from .paths import PROJECT_ROOT, DOMAIN_PATHS
from .fix_counts import DEFAULT_FIX_COUNTS, FixCounter
from .numeric_keys import convert_numeric_keys_to_ints
from .language_blocks import fix_language_blocks
from .value_parser import parse_values
from .cleaner import clean_data

__all__ = [
    "PROJECT_ROOT",
    "DOMAIN_PATHS",
    "DEFAULT_FIX_COUNTS",
    "FixCounter",
    "convert_numeric_keys_to_ints",
    "fix_language_blocks",
    "parse_values",
    "clean_data",
]

