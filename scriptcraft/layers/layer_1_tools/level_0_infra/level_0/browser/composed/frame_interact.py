"""Click/fill/press inside resolved frame context."""

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.composed.frame_wait import (
    wait_for_selector,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.frame_context import (
    get_context_for_selector,
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


def press_enter(page: Page, selector: str) -> None:
    wait_for_selector(page, selector)
    _require_context(page, selector, "press_enter").press(selector, "Enter")


def set_checkbox_checked(page: Page, selector: str, checked: bool) -> None:
    wait_for_selector(page, selector)
    _require_context(page, selector, "set_checkbox_checked").locator(
        selector
    ).set_checked(checked)
