"""Resolve Playwright Page/Frame context for a selector (iframe-aware)."""

import time

from playwright.sync_api import Frame, Page

from scriptcraft.layers.layer_0_core.level_0 import poll_until_deadline


def _context_has_selector(ctx: Page | Frame, selector: str) -> bool:
    try:
        return ctx.query_selector(selector) is not None
    except Exception:
        return False


def get_context_for_selector(page: Page, selector: str) -> Page | Frame | None:
    """Return the page or child frame that contains ``selector``, if any."""
    if _context_has_selector(page, selector):
        return page

    for frame in page.frames:
        try:
            if _context_has_selector(frame, selector):
                return frame
        except Exception:
            continue

    return None


def get_active_frame(page: Page, anchor_selector: str) -> Page | Frame:
    """Return the frame containing ``anchor_selector``, else the top-level page."""
    ctx = get_context_for_selector(page, anchor_selector)
    if ctx is not None:
        return ctx
    return page


def selector_exists(page: Page, selector: str) -> bool:
    return get_context_for_selector(page, selector) is not None


def wait_for_selector(
    page: Page,
    selector: str,
    timeout_ms: int = 100_000,
) -> None:
    deadline = time.monotonic() + (timeout_ms / 1000)

    def _wait_for_ctx() -> bool:
        ctx = get_context_for_selector(page, selector)
        if ctx is None:
            return False

        remaining_ms = int((deadline - time.monotonic()) * 1000)
        ctx.wait_for_selector(
            selector,
            timeout=max(remaining_ms, 500),
        )
        return True

    if poll_until_deadline(
        _wait_for_ctx,
        timeout_ms=timeout_ms,
        poll_ms=200,
        on_poll=page.wait_for_timeout,
    ):
        return

    raise TimeoutError(f"Timeout waiting for selector: {selector}")


def click_button(page: Page, selector: str) -> None:
    """
    Click a selector after waiting for it, resolving frame context.

    This is a tiny primitive used broadly by higher-level composed workflows.
    """
    wait_for_selector(page, selector)
    ctx = get_context_for_selector(page, selector)
    if ctx is None:
        raise RuntimeError(f"Selector not found for click_button: {selector}")
    ctx.click(selector)


def click(page: Page, selector: str) -> None:
    wait_for_selector(page, selector)
    ctx = get_context_for_selector(page, selector)
    if ctx is None:
        raise RuntimeError(f"Selector not found for click: {selector}")
    ctx.click(selector)


def fill(page: Page, selector: str, value: str) -> None:
    wait_for_selector(page, selector)
    ctx = get_context_for_selector(page, selector)
    if ctx is None:
        raise RuntimeError(f"Selector not found for fill: {selector}")
    ctx.fill(selector, value)


def clear_and_fill(page: Page, selector: str, value: str) -> None:
    wait_for_selector(page, selector)
    ctx = get_context_for_selector(page, selector)
    if ctx is None:
        raise RuntimeError(f"Selector not found for clear_and_fill: {selector}")
    ctx.fill(selector, "")
    ctx.fill(selector, value)


def fill_input(page: Page, selector: str, value: str) -> None:
    clear_and_fill(page, selector, value)
