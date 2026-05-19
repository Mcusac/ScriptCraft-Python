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

from playwright.sync_api import Frame, Page

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    LOCATION_SPYGLASS_BUTTON_SELECTOR,
    LOCATION_CODE_INPUT_SELECTOR,
    LOCATION_LOOKUP_BUTTON_SELECTOR,
    LOCATION_SEARCH_RESULT_SELECTOR,
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


def get_location_lookup_frame(page: Page) -> Frame:
    return ba.get_lookup_modal_frame(page, LOCATION_CODE_INPUT_SELECTOR)


def enter_location_code_in_frame(
    frame: Frame,
    location_code: str,
) -> None:
    formatted = ba.format_location_for_lookup(location_code)
    ba.fill_in_frame(frame, LOCATION_CODE_INPUT_SELECTOR, formatted)


def execute_location_search_in_frame(frame: Frame) -> None:
    ba.click_in_frame(frame, LOCATION_LOOKUP_BUTTON_SELECTOR)
    ba.wait_for_modal_lookup_settled(
        frame,
        LOCATION_SEARCH_RESULT_SELECTOR,
    )


def select_location_result_in_frame(
    page: Page,
    frame: Frame,
    location_code: str,
) -> None:
    formatted = ba.format_location_for_lookup(location_code)
    ba.wait_for_lookup_results_in_frame(
        frame,
        LOCATION_SEARCH_RESULT_SELECTOR,
        formatted,
    )
    ba.select_lookup_result(
        page,
        LOCATION_SEARCH_RESULT_SELECTOR,
        match_text=formatted,
        context=frame,
        modal_anchor_selector=LOCATION_CODE_INPUT_SELECTOR,
    )


def enter_location_code(page: Page, location_code: str) -> None:
    """
    Enters location code into modal input.
    """
    frame = get_location_lookup_frame(page)
    enter_location_code_in_frame(frame, location_code)


def execute_location_search(page: Page) -> None:
    """
    Executes lookup search in modal.
    """
    frame = get_location_lookup_frame(page)
    execute_location_search_in_frame(frame)


def select_location_result(page: Page, location_code: str) -> None:
    """
    Selects lookup row whose link text matches location_code.
    """
    frame = get_location_lookup_frame(page)
    select_location_result_in_frame(page, frame, location_code)


def complete_location_lookup(page: Page, location_code: str) -> None:
    """
    Full location lookup workflow:
    open → enter → search → select (all scoped to modal frame)
    """
    open_location_lookup_modal(page)
    frame = get_location_lookup_frame(page)
    enter_location_code_in_frame(frame, location_code)
    execute_location_search_in_frame(frame)
    frame = get_location_lookup_frame(page)
    select_location_result_in_frame(page, frame, location_code)


