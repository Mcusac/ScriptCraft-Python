"""Auto-generated mixed exports."""


from . import (
    cv_splits,
    domain,
    io,
    processing,
)

from .cv_splits import *
from .domain import *
from .io import *
from .processing import *

from .debug_render import (
    debug_merge,
    debug_raw_inputs,
)

from .flagged_indices import (
    IndexLike,
    flag_indices,
)

from .tabular_diagnostics import (
    compare_column_dtypes,
    describe_numeric,
    drop_empty_columns,
    find_duplicate_rows,
    find_non_numeric,
    get_column_dtypes,
    get_column_letter,
    get_column_stats,
    get_common_columns,
    to_numeric_safe,
)

__all__ = (
    list(cv_splits.__all__)
    + list(domain.__all__)
    + list(io.__all__)
    + list(processing.__all__)
    + [
        "IndexLike",
        "compare_column_dtypes",
        "debug_merge",
        "debug_raw_inputs",
        "describe_numeric",
        "drop_empty_columns",
        "find_duplicate_rows",
        "find_non_numeric",
        "flag_indices",
        "get_column_dtypes",
        "get_column_letter",
        "get_column_stats",
        "get_common_columns",
        "to_numeric_safe",
    ]
)
