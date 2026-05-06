"""Auto-generated mixed exports."""


from . import detection

from .detection import *

from .location_normalizer import (
    enforce_spacing,
    extract_location_parts,
    normalize_building_codes,
    normalize_location,
    normalize_off_campus,
    normalize_whitespace,
    rebuild_location,
    remove_hyphens,
    strip_room_noise,
)

from .merge import build_device_merged

__all__ = (
    list(detection.__all__)
    + [
        "build_device_merged",
        "enforce_spacing",
        "extract_location_parts",
        "normalize_building_codes",
        "normalize_location",
        "normalize_off_campus",
        "normalize_whitespace",
        "rebuild_location",
        "remove_hyphens",
        "strip_room_noise",
    ]
)
