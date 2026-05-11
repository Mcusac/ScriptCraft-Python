"""Auto-generated package exports."""


from .change_detector import (
    detect_custodian_changes,
    detect_location_changes,
)

from .debug_hooks import (
    emit_input_debug,
    emit_merge_debug,
)

from .form_reshape import reshape_form_wide_to_long

from .key_semantics import (
    finalize_merge_key,
    normalize_merge_key_value,
)

from .location_transforms import (
    enforce_spacing,
    normalize_building_codes,
    normalize_off_campus,
    normalize_whitespace,
    remove_hyphens,
    strip_room_noise,
)

from .tag_pipeline import (
    normalize_employee_id,
    normalize_tag,
)

from .transforms import (
    project_final_tag,
    rename_asset_columns,
    rename_form_columns,
)

from .validation import (
    require_columns,
    validate_merge_inputs,
)

__all__ = [
    "detect_custodian_changes",
    "detect_location_changes",
    "emit_input_debug",
    "emit_merge_debug",
    "enforce_spacing",
    "finalize_merge_key",
    "normalize_building_codes",
    "normalize_employee_id",
    "normalize_merge_key_value",
    "normalize_off_campus",
    "normalize_tag",
    "normalize_whitespace",
    "project_final_tag",
    "remove_hyphens",
    "rename_asset_columns",
    "rename_form_columns",
    "require_columns",
    "reshape_form_wide_to_long",
    "strip_room_noise",
    "validate_merge_inputs",
]
