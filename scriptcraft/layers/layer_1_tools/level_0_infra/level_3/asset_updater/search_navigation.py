from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    ASSET_ID_INPUT_SELECTOR,
    RETURN_TO_SEARCH_BUTTON_SELECTOR,
    SEARCH_BUTTON_SELECTOR,
    TAG_NUMBER_INPUT_SELECTOR,
    click_button,
    safe_wait,
    wait_for_page_load,
    wait_for_selector,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import clear_field
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import dismiss_message_modals


def click_search(page: Page) -> None:
    click_button(page, SEARCH_BUTTON_SELECTOR)
    wait_for_page_load(page)


def prepare_search_for_next_row(page: Page) -> None:
    dismiss_message_modals(page)
    clear_field(page, TAG_NUMBER_INPUT_SELECTOR)
    clear_field(page, ASSET_ID_INPUT_SELECTOR)
    safe_wait(page, 300)


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

