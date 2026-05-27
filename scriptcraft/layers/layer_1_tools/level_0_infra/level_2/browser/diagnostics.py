"""Logging-backed selector wait diagnostics."""

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    get_context_for_selector,
    get_page_title,
    get_page_url,
    log_and_print,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import wait_for_selector


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
            f"[DIAGNOSTIC] Selector exists: {get_context_for_selector(page, selector) is not None}"
        )
        log_and_print(f"[DIAGNOSTIC] Error: {e}\n")
        raise

