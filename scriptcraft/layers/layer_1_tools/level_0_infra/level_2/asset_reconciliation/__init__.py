"""Auto-generated package exports."""


from .change_detector import (
    detect_custodian_changes,
    detect_location_changes,
)

from .form_reshape import reshape_form_wide_to_long

from .key_normalizer import normalize_merge_key

from .location_transforms import (
    enforce_spacing,
    normalize_building_codes,
    normalize_off_campus,
    normalize_whitespace,
    remove_hyphens,
    strip_room_noise,
)

from .validation import validate_merge_inputs

__all__ = [
    "detect_custodian_changes",
    "detect_location_changes",
    "enforce_spacing",
    "normalize_building_codes",
    "normalize_merge_key",
    "normalize_off_campus",
    "normalize_whitespace",
    "remove_hyphens",
    "reshape_form_wide_to_long",
    "strip_room_noise",
    "validate_merge_inputs",
]
