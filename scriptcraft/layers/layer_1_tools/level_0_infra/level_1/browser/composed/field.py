"""Clear/reset field helpers (frame-aware)."""

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    click_button,
    get_context_for_selector,
    wait_for_selector,
    wait_for_page_load,
)


def clear_field(page: Page, selector: str) -> None:
    ctx = get_context_for_selector(page, selector)
    if ctx is None:
        wait_for_selector(page, selector)
        ctx = get_context_for_selector(page, selector)
    if ctx is None:
        raise RuntimeError(f"Selector not found for clear_field: {selector}")
    ctx.fill(selector, "")


def reset_and_search(
    page: Page,
    asset_id_selector: str,
    search_button_selector: str,
) -> None:
    clear_field(page, asset_id_selector)
    click_button(page, search_button_selector)
    wait_for_page_load(page)

