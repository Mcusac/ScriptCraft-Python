"""Auto-generated package exports."""


from .browser import launch_browser

from .constants import (
    AGE_PERIOD_HEADER,
    AGE_PERIOD_TO_PANEL_INDEX,
    BLOCK_COLUMNS,
    FIELD_LABEL_MAPS,
)

from .data import (
    build_address_data,
    build_panels_data,
    get_age_period_suffixes,
    get_panel_index,
    is_real_address,
)

from .language import detect_form_language

from .panel_filler import (
    ensure_address_blocks,
    fill_all_blocks,
    fill_checkbox,
    fill_input_field,
    fill_panel,
    fill_single_block,
    get_panel_element,
    open_panel,
    remove_extra_address_blocks,
)

__all__ = [
    "AGE_PERIOD_HEADER",
    "AGE_PERIOD_TO_PANEL_INDEX",
    "BLOCK_COLUMNS",
    "FIELD_LABEL_MAPS",
    "build_address_data",
    "build_panels_data",
    "detect_form_language",
    "ensure_address_blocks",
    "fill_all_blocks",
    "fill_checkbox",
    "fill_input_field",
    "fill_panel",
    "fill_single_block",
    "get_age_period_suffixes",
    "get_panel_element",
    "get_panel_index",
    "is_real_address",
    "launch_browser",
    "open_panel",
    "remove_extra_address_blocks",
]
