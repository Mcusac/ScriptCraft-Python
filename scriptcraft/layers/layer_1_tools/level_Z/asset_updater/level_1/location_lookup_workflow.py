# ============================================================
# location_lookup_workflow.py — LEVEL_1
#
# PURPOSE:
# - Encapsulates ONLY the Location Lookup modal workflow
# - Uses Level_0 browser primitives
# - Uses constants only
#
# DOES NOT:
# - Load CSVs
# - Decide which tag to process
# - Handle custodians
# - Perform asset updates
# ============================================================

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    browser_actions as ba,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0.constants import (
    LOCATION_SPYGLASS_BUTTON_SELECTOR,
    LOCATION_CODE_INPUT_SELECTOR,
    LOCATION_LOOKUP_BUTTON_SELECTOR,
    LOCATION_SEARCH_RESULT_SELECTOR,
    DATE_OF_TRANSFER_INPUT_SELECTOR,
)


# ============================================================
# LOCATION LOOKUP WORKFLOW
# ============================================================

def open_location_lookup_modal(page: Page) -> None:
    """
    Opens the location lookup modal via spyglass icon.
    """
    ba.click_button(page, LOCATION_SPYGLASS_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)


def enter_location_code(page: Page, location_code: str) -> None:
    """
    Enters location code into modal input.
    """
    ba.fill_input(page, LOCATION_CODE_INPUT_SELECTOR, location_code)


def execute_location_search(page: Page) -> None:
    """
    Executes lookup search in modal.
    """
    ba.click_button(page, LOCATION_LOOKUP_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)


def select_location_result(page: Page) -> None:
    """
    Selects first matching location result.
    """
    ba.select_lookup_result(page, LOCATION_SEARCH_RESULT_SELECTOR)


def complete_location_lookup(page: Page, location_code: str) -> None:
    """
    Full location lookup workflow:
    open → enter → search → select
    """
    open_location_lookup_modal(page)
    enter_location_code(page, location_code)
    execute_location_search(page)
    select_location_result(page)


# ============================================================
# DATE OF TRANSFER (kept here because it is tightly coupled
# to this page state flow in your current design)
# ============================================================

def set_transfer_date_to_today(page: Page) -> None:
    """
    Fills transfer date with current system date.
    """
    ba.fill_current_date(page, DATE_OF_TRANSFER_INPUT_SELECTOR)