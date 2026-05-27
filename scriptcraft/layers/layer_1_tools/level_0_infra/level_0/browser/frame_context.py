"""Resolve Playwright Page/Frame context for a selector (iframe-aware)."""

from playwright.sync_api import Frame, Page


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
