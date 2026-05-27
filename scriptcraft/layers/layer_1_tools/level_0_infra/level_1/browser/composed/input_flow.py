"""Higher-level input sequences composed from frame interact + dates."""

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    get_current_date_mmddyyyy,
    get_context_for_selector,
    wait_for_selector,
)


def _require_context(page: Page, selector: str, action: str):
    ctx = get_context_for_selector(page, selector)
    if ctx is None:
        raise RuntimeError(f"Selector not found for {action}: {selector}")
    return ctx


def click(page: Page, selector: str) -> None:
    wait_for_selector(page, selector)
    _require_context(page, selector, "click").click(selector)


def fill(page: Page, selector: str, value: str) -> None:
    wait_for_selector(page, selector)
    _require_context(page, selector, "fill").fill(selector, value)


def clear_and_fill(page: Page, selector: str, value: str) -> None:
    wait_for_selector(page, selector)
    ctx = _require_context(page, selector, "clear_and_fill")
    ctx.fill(selector, "")
    ctx.fill(selector, value)


def fill_input(page: Page, selector: str, value: str) -> None:
    clear_and_fill(page, selector, value)


def click_and_fill(page: Page, selector: str, value: str) -> None:
    click(page, selector)
    fill(page, selector, value)


def click_button(page: Page, selector: str) -> None:
    click(page, selector)


def submit(page: Page, selector: str) -> None:
    click_button(page, selector)


def fill_current_date(page: Page, selector: str) -> None:
    fill_input(page, selector, get_current_date_mmddyyyy())

