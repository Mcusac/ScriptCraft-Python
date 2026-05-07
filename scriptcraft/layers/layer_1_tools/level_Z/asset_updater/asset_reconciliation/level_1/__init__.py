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

from .form_debug import debug_form

from .form_utils import (
    build_full_name,
    extract_device_columns,
    resolve_column,
    safe_get,
)

from .key_normalizer import (
    normalize_merge_key,
    prepare_merge_keys,
)

from .location_normalizer import (
    enforce_spacing,
    normalize_building_codes,
    normalize_location,
    normalize_off_campus,
    normalize_whitespace,
    remove_hyphens,
    strip_room_noise,
)

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
        "debug_form",
        "debug_merge",
        "debug_raw_inputs",
        "enforce_spacing",
        "extract_device_columns",
        "filter_computers_only",
        "normalize_building_codes",
        "normalize_location",
        "normalize_merge_key",
        "normalize_off_campus",
        "normalize_whitespace",
        "prepare_merge_keys",
        "remove_hyphens",
        "require_columns",
        "require_exact_columns",
        "resolve_column",
        "safe_get",
        "strip_room_noise",
    ]
)
