"""
RHQ Form Autofiller (level_0).

This package contains the focused building blocks used by the RHQ form autofiller tool:
- data extraction/transforms from the input spreadsheet
- selenium browser launch helpers
- form language detection and form-filling primitives
"""

from .browser import launch_browser
from .data import build_address_data
from .language import detect_form_language
from .panel_filler import fill_panel

__all__ = [
    "build_address_data",
    "detect_form_language",
    "fill_panel",
    "launch_browser",
]

