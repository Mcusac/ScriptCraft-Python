"""Logging-backed selector wait diagnostics."""

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.composed.frame_wait import (
    selector_exists,
    wait_for_selector,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.primitives.page_state import (
    get_page_title,
    get_page_url,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print


def log_page_state(page: Page, prefix: str = "") -> None:
    log_and_print(f"{prefix} URL: {get_page_url(page)}")
    log_and_print(f"{prefix} Title: {get_page_title(page)}")


def wait_for_selector_with_diagnostics(
    page: Page,
    selector: str,
    timeout_ms: int = 100_000,
) -> None:
    try:
        wait_for_selector(page, selector, timeout_ms)
    except Exception as e:
        log_and_print(f"\n[DIAGNOSTIC] Selector wait failed: {selector}")
        log_page_state(page, "[DIAGNOSTIC]")
        log_and_print(
            f"[DIAGNOSTIC] Selector exists: {selector_exists(page, selector)}"
        )
        log_and_print(f"[DIAGNOSTIC] Error: {e}\n")
        raise
