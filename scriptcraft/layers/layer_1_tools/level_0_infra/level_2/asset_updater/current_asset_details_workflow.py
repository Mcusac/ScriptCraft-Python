# current_asset_details_workflow.py — LEVEL_1

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    format_location_for_lookup,
    CURRENT_ASSET_EMPLOYEE_ID_SELECTOR,
    CURRENT_ASSET_LOCATION_CODE_SELECTOR,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    get_display_text,
)

def read_current_location_code(page: Page) -> str:
    """
    Location code from Current Asset Details (for custodian-only updates).
    """
    raw = get_display_text(
        page,
        CURRENT_ASSET_LOCATION_CODE_SELECTOR,
        normalize_whitespace=True,
    )
    return format_location_for_lookup(raw)


def read_current_employee_id(page: Page) -> str:
    """
    Employee ID from Current Asset Details (for location-only updates).
    """
    return get_display_text(
        page,
        CURRENT_ASSET_EMPLOYEE_ID_SELECTOR,
        normalize_whitespace=False,
    )
