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

from .debug_print import (
    debug_merge,
    debug_raw_inputs,
)

from .detect_missing_from_form import detect_missing_from_form

from .detect_off_campus import detect_off_campus

from .detect_only_in_form import detect_only_in_form

from .form_debug import debug_form

from .form_utils import (
    build_full_name,
    extract_device_columns,
    resolve_column,
    safe_get,
)

from .location_primitives import (
    collapse_whitespace,
    to_string_dtype,
)

from .merge_contracts import validate_merged_contract

from .sanity_checks import run_sanity_checks

from .tag_sanitizer import sanitize_tag

from .text_canonicalizer import canonical_text

from .validators import (
    assert_asset_raw,
    assert_form_normalized,
    assert_form_raw,
    assert_merged,
    require_columns,
    require_exact_columns,
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
        "debug_merge",
        "debug_raw_inputs",
        "detect_missing_from_form",
        "detect_off_campus",
        "detect_only_in_form",
        "extract_device_columns",
        "filter_computers_only",
        "require_columns",
        "require_exact_columns",
        "resolve_column",
        "run_sanity_checks",
        "safe_get",
        "sanitize_tag",
        "to_string_dtype",
        "validate_merged_contract",
    ]
)
