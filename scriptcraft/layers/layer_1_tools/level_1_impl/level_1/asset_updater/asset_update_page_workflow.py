# ============================================================
# asset_update_page_workflow.py — LEVEL_1
#
# PURPOSE:
# - Handles ONLY main Asset Update page interactions
# - Does NOT include modal workflows (location/custodian)
# - Does NOT orchestrate full asset update flow
#
# DESIGN:
# - Page-level atomic actions only
# - Composable for Level_2 orchestrator
# ============================================================

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    BUSINESS_UNIT_INPUT_SELECTOR,
    TAG_NUMBER_INPUT_SELECTOR,
    UPDATE_THIS_ASSET_BUTTON_SELECTOR,
    RETURN_TO_SEARCH_BUTTON_SELECTOR,
    ASSET_ID_INPUT_SELECTOR,
    SEARCH_BUTTON_SELECTOR,
    BUSINESS_UNIT_VALUE,
)


# ============================================================
# PAGE INITIALIZATION / SEARCH CONTROLS
# ============================================================

def set_business_unit(page: Page) -> None:
    """
    Sets fixed business unit (HS763).
    """
    ba.fill_input(page, BUSINESS_UNIT_INPUT_SELECTOR, BUSINESS_UNIT_VALUE)


def enter_tag_number(page: Page, tag_number: str) -> None:
    """
    Enters asset tag number into search field.
    """
    ba.fill_input(page, TAG_NUMBER_INPUT_SELECTOR, tag_number)


def click_search(page: Page) -> None:
    """
    Executes asset search.
    """
    ba.click_button(page, SEARCH_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)


def reset_asset_id_field(page: Page) -> None:
    """
    Clears asset ID field before next iteration.
    """
    ba.clear_field(page, ASSET_ID_INPUT_SELECTOR)


def prepare_search_for_next_row(page: Page) -> None:
    """
    Reset search form after a row failure so the next tag search can run.
    """
    ba.dismiss_message_modals(page)
    ba.clear_field(page, TAG_NUMBER_INPUT_SELECTOR)
    ba.clear_field(page, ASSET_ID_INPUT_SELECTOR)
    ba.safe_wait(page, 300)


# ============================================================
# ASSET UPDATE FIELDS
# ============================================================


# ============================================================
# FINAL ACTIONS
# ============================================================

def submit_asset_update(page: Page) -> None:
    """
    Submits asset update.
    """
    ba.click_button(page, UPDATE_THIS_ASSET_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)


def confirm_update_ok(page: Page) -> None:
    """
    Confirms success modal.
    """
    ba.click_button(page, '[id="#ICOK"]')
    ba.wait_for_page_load(page)


def return_to_search(page: Page) -> None:
    """
    Returns to search screen after update.
    """
    ba.click_button(page, RETURN_TO_SEARCH_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)


def return_to_search_after_failure(page: Page) -> None:
    """
    Return to search after a row failure without networkidle (avoids long hangs).
    """
    ba.click_button(page, RETURN_TO_SEARCH_BUTTON_SELECTOR)

    try:
        page.wait_for_load_state("domcontentloaded", timeout=15_000)
    except Exception:
        pass

    ba.wait_for_selector(
        page,
        TAG_NUMBER_INPUT_SELECTOR,
        timeout_ms=30_000,
    )


# ============================================================
# PAGE RESET FLOW (SAFE LOOP SUPPORT)
# ============================================================

def reset_search_state(page: Page) -> None:
    """
    Prepares page for next iteration:
    - clears asset id
    - ready for new search
    """
    reset_asset_id_field(page)
    click_search(page)