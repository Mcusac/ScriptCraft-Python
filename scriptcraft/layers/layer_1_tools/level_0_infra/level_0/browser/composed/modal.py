"""Optional modal click/wait built from frame wait + navigation + poll."""

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.composed.frame_wait import (
    wait_for_selector,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.composed.input_flow import (
    click_button,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.frame_context import (
    get_context_for_selector,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.primitives.navigation import (
    wait_for_page_load,
)
from scriptcraft.layers.layer_0_core.level_0 import poll_until_deadline


def wait_for_modal(page: Page, selector: str = "div[role='dialog']") -> None:
    wait_for_selector(page, selector)


def close_modal(page: Page, selector: str) -> None:
    click_button(page, selector)


def click_button_if_present(
    page: Page,
    selector: str,
    timeout_ms: int = 5_000,
) -> bool:
    def _try_click() -> bool:
        ctx = get_context_for_selector(page, selector)
        if ctx is None:
            return False
        try:
            ctx.click(selector)
            wait_for_page_load(page)
            return True
        except Exception:
            return False

    return poll_until_deadline(
        _try_click,
        timeout_ms=timeout_ms,
        poll_ms=200,
        on_poll=page.wait_for_timeout,
    )
