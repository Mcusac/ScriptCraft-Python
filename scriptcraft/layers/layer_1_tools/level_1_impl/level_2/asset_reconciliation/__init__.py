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
)

from .validation import (
    validate_merge_inputs,
)

__all__ = [
    "detect_custodian_changes",
    "detect_location_changes",
    "emit_input_debug",
    "emit_merge_debug",
    "enforce_spacing",
    "normalize_building_codes",
    "normalize_employee_id",
    "normalize_merge_key_value",
    "normalize_off_campus",
    "normalize_tag",
    "normalize_whitespace",
    "project_final_tag",
    "remove_hyphens",
    "reshape_form_wide_to_long",
    "strip_room_noise",
    "validate_merge_inputs",
]
