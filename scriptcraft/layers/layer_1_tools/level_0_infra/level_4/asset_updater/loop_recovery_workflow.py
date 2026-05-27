from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    log_and_print,
    selector_exists,
    UPDATE_THIS_ASSET_BUTTON_SELECTOR,
    TAG_NUMBER_INPUT_SELECTOR,
    BUSINESS_UNIT_INPUT_SELECTOR,
    SEARCH_BUTTON_SELECTOR,
    RETURN_TO_SEARCH_BUTTON_SELECTOR,
    LOOKUP_MODAL_CANCEL_SELECTOR,
    ASSET_URL,
    wait_until_page_condition,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    click_ok_if_present,
    is_open_lookup_modal_frame,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    prepare_search_for_next_row,
    return_to_search_after_failure,
    wait_for_post_auth_ready,
)

SEARCH_PAGE_POLL_MS = 200
SEARCH_PAGE_WAIT_MS = 30_000
GOTO_SEARCH_WAIT_MS = 15_000


def is_on_asset_search_page(page: Page) -> bool:
    """
    True when on the asset search screen (not the update form).
    """
    if selector_exists(page, UPDATE_THIS_ASSET_BUTTON_SELECTOR):
        return False

    if not selector_exists(page, TAG_NUMBER_INPUT_SELECTOR):
        return False

    if not selector_exists(page, BUSINESS_UNIT_INPUT_SELECTOR):
        return False

    return selector_exists(page, SEARCH_BUTTON_SELECTOR)


def wait_for_asset_search_page(
    page: Page,
    timeout_ms: int = SEARCH_PAGE_WAIT_MS,
) -> bool:
    """Poll until the search screen is ready or timeout."""
    return wait_until_page_condition(
        page,
        lambda: is_on_asset_search_page(page),
        timeout_ms=timeout_ms,
        poll_ms=SEARCH_PAGE_POLL_MS,
    )


def _dismiss_lookup_modals(page: Page) -> None:
    for frame in page.frames:
        if not is_open_lookup_modal_frame(frame):
            continue

        try:
            cancel = frame.query_selector(LOOKUP_MODAL_CANCEL_SELECTOR)
            if cancel is not None:
                cancel.click()
                page.wait_for_timeout(300)
        except Exception:
            pass


def _safe_step(step_name: str, action) -> None:
    try:
        action()
    except Exception as exc:
        log_and_print(f"[RECOVERY] {step_name} skipped: {exc}")


def _try_goto_asset_search(page: Page) -> bool:
    """
    Full reload only when return-to-search is unavailable (rare).
    """
    log_and_print("[RECOVERY] Navigating to asset URL (last resort)...")

    try:
        page.goto(
            ASSET_URL,
            wait_until="domcontentloaded",
            timeout=GOTO_SEARCH_WAIT_MS,
        )
    except Exception as exc:
        log_and_print(f"[RECOVERY] goto skipped: {exc}")
        return False

    if wait_for_asset_search_page(page, GOTO_SEARCH_WAIT_MS):
        prepare_search_for_next_row(page)
        return True

    try:
        wait_for_post_auth_ready(page, timeout_ms=30_000)
    except Exception as exc:
        log_and_print(f"[RECOVERY] post-auth wait skipped: {exc}")

    if wait_for_asset_search_page(page, GOTO_SEARCH_WAIT_MS):
        prepare_search_for_next_row(page)
        return True

    return False


def recover_to_asset_search(page: Page) -> bool:
    """
    Best-effort return to the asset search screen after a row failure.
    Returns True when the next row can run a tag search.
    """
    _safe_step("dismiss lookup modals", lambda: _dismiss_lookup_modals(page))
    _safe_step("dismiss OK dialog", lambda: click_ok_if_present(page))

    if selector_exists(page, RETURN_TO_SEARCH_BUTTON_SELECTOR):
        _safe_step(
            "return to search",
            lambda: return_to_search_after_failure(page),
        )
    else:
        _safe_step(
            "dismiss lookup modals (retry)",
            lambda: _dismiss_lookup_modals(page),
        )

    if wait_for_asset_search_page(page, SEARCH_PAGE_WAIT_MS):
        prepare_search_for_next_row(page)
        return True

    if selector_exists(page, RETURN_TO_SEARCH_BUTTON_SELECTOR):
        log_and_print(
            "[RECOVERY] Update page still visible after return to search"
        )
        return False

    return _try_goto_asset_search(page)
