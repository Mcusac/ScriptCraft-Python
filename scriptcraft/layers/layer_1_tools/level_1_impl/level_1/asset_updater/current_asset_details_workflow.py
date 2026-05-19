# current_asset_details_workflow.py — LEVEL_1

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    CURRENT_ASSET_EMPLOYEE_ID_SELECTOR,
    CURRENT_ASSET_LOCATION_CODE_SELECTOR,
)


def read_current_location_code(page: Page) -> str:
    """
    Location code from Current Asset Details (for custodian-only updates).
    """
    raw = ba.get_display_text(
        page,
        CURRENT_ASSET_LOCATION_CODE_SELECTOR,
        normalize_whitespace=True,
    )
    return ba.format_location_for_lookup(raw)


def read_current_employee_id(page: Page) -> str:
    """
    Employee ID from Current Asset Details (for location-only updates).
    """
    return ba.get_display_text(
        page,
        CURRENT_ASSET_EMPLOYEE_ID_SELECTOR,
        normalize_whitespace=False,
    )
