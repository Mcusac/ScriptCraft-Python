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

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    clear_field,
    click_button,
    fill_input,
    safe_wait,
    wait_for_page_load,
    wait_for_selector,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    ASSET_ID_INPUT_SELECTOR,
    BUSINESS_UNIT_INPUT_SELECTOR,
    BUSINESS_UNIT_VALUE,
    RETURN_TO_SEARCH_BUTTON_SELECTOR,
    SEARCH_BUTTON_SELECTOR,
    TAG_NUMBER_INPUT_SELECTOR,
    UPDATE_THIS_ASSET_BUTTON_SELECTOR,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    dismiss_message_modals,
)


def set_business_unit(page: Page) -> None:
    fill_input(page, BUSINESS_UNIT_INPUT_SELECTOR, BUSINESS_UNIT_VALUE)


def enter_tag_number(page: Page, tag_number: str) -> None:
    fill_input(page, TAG_NUMBER_INPUT_SELECTOR, tag_number)


def click_search(page: Page) -> None:
    click_button(page, SEARCH_BUTTON_SELECTOR)
    wait_for_page_load(page)


def reset_asset_id_field(page: Page) -> None:
    clear_field(page, ASSET_ID_INPUT_SELECTOR)


def prepare_search_for_next_row(page: Page) -> None:
    dismiss_message_modals(page)
    clear_field(page, TAG_NUMBER_INPUT_SELECTOR)
    clear_field(page, ASSET_ID_INPUT_SELECTOR)
    safe_wait(page, 300)


def submit_asset_update(page: Page) -> None:
    click_button(page, UPDATE_THIS_ASSET_BUTTON_SELECTOR)
    wait_for_page_load(page)


def confirm_update_ok(page: Page) -> None:
    click_button(page, '[id="#ICOK"]')
    wait_for_page_load(page)


def return_to_search(page: Page) -> None:
    click_button(page, RETURN_TO_SEARCH_BUTTON_SELECTOR)
    wait_for_page_load(page)


def return_to_search_after_failure(page: Page) -> None:
    click_button(page, RETURN_TO_SEARCH_BUTTON_SELECTOR)
    try:
        page.wait_for_load_state("domcontentloaded", timeout=15_000)
    except Exception:
        pass
    wait_for_selector(
        page,
        TAG_NUMBER_INPUT_SELECTOR,
        timeout_ms=30_000,
    )


def reset_search_state(page: Page) -> None:
    reset_asset_id_field(page)
    click_search(page)
