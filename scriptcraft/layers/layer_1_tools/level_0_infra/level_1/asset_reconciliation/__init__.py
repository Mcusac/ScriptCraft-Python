"""Auto-generated mixed exports."""


from . import detection

from .detection import *

from .asset_filters import filter_computers_only

from .contracts import (
    ASSET_REQUIRED_COLUMNS,
    ASSET_TO_MERGED_MAP,
    FORM_REQUIRED_COLUMNS,
    FORM_TO_MERGED_MAP,
)

from .debug_hooks import (
    emit_input_debug,
    emit_merge_debug,
)

from .form_debug import debug_form

from .form_utils import (
    build_full_name,
    extract_device_columns,
    resolve_column,
    safe_get,
)

from .key_semantics import normalize_merge_key_value

from .location_primitives import (
    collapse_whitespace,
    to_string_dtype,
)

from .sanity_checks import run_sanity_checks

from .tag_pipeline import (
    normalize_employee_id,
    normalize_tag,
)

from .text_canonicalizer import canonical_text

from .validators import (
    assert_asset_raw,
    assert_form_normalized,
    assert_form_raw,
    assert_merged,
)

__all__ = (
    list(detection.__all__)
    + [
        "ASSET_REQUIRED_COLUMNS",
        "ASSET_TO_MERGED_MAP",
        "FORM_REQUIRED_COLUMNS",
        "FORM_TO_MERGED_MAP",
        "assert_asset_raw",
        "assert_form_normalized",
        "assert_form_raw",
        "assert_merged",
        "build_full_name",
        "canonical_text",
        "collapse_whitespace",
        "debug_form",
        "emit_input_debug",
        "emit_merge_debug",
        "extract_device_columns",
        "filter_computers_only",
        "normalize_employee_id",
        "normalize_merge_key_value",
        "normalize_tag",
        "resolve_column",
        "run_sanity_checks",
        "safe_get",
        "to_string_dtype",
    ]
)
