"""PeopleSoft asset-updater browser bindings (constants + shell anchor only)."""

from playwright.sync_api import Frame, Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    EMPLOYEE_ID_INPUT_SELECTOR,
    LOCATION_CODE_INPUT_SELECTOR,
    OK_BUTTON_SELECTOR,
    TERMS_ACCEPT_BUTTON_SELECTOR,
    TERMS_MODAL_APPEAR_DELAY_MS,
    get_active_frame,
    get_context_for_selector,
    is_lookup_modal_frame,
    normalize_lookup_text,
    wait_for_selector,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    click_button_if_present,
    select_lookup_result as select_lookup_result_impl,
)

_LOOKUP_INPUT_SELECTORS = (
    LOCATION_CODE_INPUT_SELECTOR,
    EMPLOYEE_ID_INPUT_SELECTOR,
)


def click_ok_if_present(page: Page, timeout_ms: int = 5_000) -> bool:
    return click_button_if_present(page, OK_BUTTON_SELECTOR, timeout_ms=timeout_ms)


def dismiss_message_modals(
    page: Page,
    *,
    max_attempts: int = 5,
    delay_ms: int = 300,
) -> int:
    dismissed = 0
    for _ in range(max_attempts):
        if not click_ok_if_present(page, timeout_ms=2_000):
            break
        dismissed += 1
        page.wait_for_timeout(delay_ms)
    return dismissed


def click_terms_accept_if_present(
    page: Page,
    timeout_ms: int = 10_000,
) -> bool:
    page.wait_for_timeout(TERMS_MODAL_APPEAR_DELAY_MS)
    return click_button_if_present(
        page,
        TERMS_ACCEPT_BUTTON_SELECTOR,
        timeout_ms=timeout_ms,
    )


def is_open_lookup_modal_frame(frame: Frame) -> bool:
    return is_lookup_modal_frame(frame, *_LOOKUP_INPUT_SELECTORS)


def select_lookup_result(
    page: Page,
    result_selector: str,
    match_text: str | None = None,
    *,
    context: Frame | None = None,
    modal_anchor_selector: str | None = None,
) -> None:
    select_lookup_result_impl(
        page,
        result_selector,
        match_text,
        context=context,
        modal_anchor_selector=modal_anchor_selector,
        lookup_input_selectors=_LOOKUP_INPUT_SELECTORS,
    )


def get_display_text(
    page: Page,
    selector: str,
    *,
    normalize_whitespace: bool = True,
    timeout_ms: int = 30_000,
) -> str:
    wait_for_selector(page, selector, timeout_ms=timeout_ms)
    ctx = get_context_for_selector(page, selector)
    if ctx is None:
        raise RuntimeError(
            f"Selector not found for get_display_text: {selector}"
        )
    text = ctx.locator(selector).inner_text(timeout=timeout_ms).strip()
    if normalize_whitespace:
        return normalize_lookup_text(text)
    return text


def click_ctx(page: Page, selector: str) -> None:
    get_active_frame(page).click(selector)


def fill_ctx(page: Page, selector: str, value: str) -> None:
    get_active_frame(page).fill(selector, value)


def wait_for_selector_ctx(
    page: Page,
    selector: str,
    timeout_ms: int = 100_000,
) -> None:
    get_active_frame(page).wait_for_selector(selector, timeout=timeout_ms)

