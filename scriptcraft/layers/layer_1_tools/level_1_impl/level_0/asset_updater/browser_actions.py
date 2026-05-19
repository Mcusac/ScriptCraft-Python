# ============================================================
# browser_actions.py — LEVEL_0 BROWSER PRIMITIVES
#
# PURPOSE:
# - Low-level browser interaction only
# - No business logic
# - No data transformations
# - No workflow assumptions
#
# DESIGN:
# - Composable atomic actions
# - Reusable across pages/modals
# - Playwright-first patterns
# ============================================================

import time
from datetime import datetime

from playwright.sync_api import Frame, Locator, Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import (
    log_and_print,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    constants as c,
)

# ============================================================
# FRAME / CONTEXT RESOLUTION
# ============================================================


def _context_has_selector(
    ctx: Page | Frame,
    selector: str,
) -> bool:

    try:
        return ctx.query_selector(selector) is not None
    except Exception:
        return False


def get_context_for_selector(
    page: Page,
    selector: str,
) -> Page | Frame | None:

    if _context_has_selector(page, selector):
        return page

    for frame in page.frames:

        try:

            if _context_has_selector(frame, selector):
                return frame

        except Exception:
            continue

    return None


def get_active_frame(page: Page) -> Page | Frame:
    """
    Finds the frame that contains the PeopleSoft app shell.
    """

    ctx = get_context_for_selector(
        page,
        c.BUSINESS_UNIT_INPUT_SELECTOR,
    )

    if ctx is not None:
        return ctx

    return page


# ============================================================
# NAVIGATION
# ============================================================


def navigate(page: Page, url: str) -> None:
    page.goto(url)


def wait_for_page_load(page: Page, timeout_ms: int = 100_000) -> None:
    page.wait_for_load_state("networkidle", timeout=timeout_ms)


def wait_for_selector(
    page: Page,
    selector: str,
    timeout_ms: int = 100_000,
) -> None:

    deadline = time.monotonic() + (timeout_ms / 1000)

    while time.monotonic() < deadline:

        ctx = get_context_for_selector(page, selector)

        if ctx is not None:

            remaining_ms = int(
                (deadline - time.monotonic()) * 1000
            )

            ctx.wait_for_selector(
                selector,
                timeout=max(remaining_ms, 500),
            )

            return

        page.wait_for_timeout(200)

    raise TimeoutError(
        f"Timeout waiting for selector: {selector}"
    )


# ============================================================
# BASIC INTERACTIONS
# ============================================================


def click(page: Page, selector: str) -> None:

    wait_for_selector(page, selector)

    ctx = get_context_for_selector(page, selector)

    if ctx is None:
        raise RuntimeError(
            f"Selector not found for click: {selector}"
        )

    ctx.click(selector)


def fill(page: Page, selector: str, value: str) -> None:

    wait_for_selector(page, selector)

    ctx = get_context_for_selector(page, selector)

    if ctx is None:
        raise RuntimeError(
            f"Selector not found for fill: {selector}"
        )

    ctx.fill(selector, value)


def clear_and_fill(page: Page, selector: str, value: str) -> None:

    wait_for_selector(page, selector)

    ctx = get_context_for_selector(page, selector)

    if ctx is None:
        raise RuntimeError(
            f"Selector not found for clear_and_fill: {selector}"
        )

    ctx.fill(selector, "")
    ctx.fill(selector, value)


def press_enter(page: Page, selector: str) -> None:

    wait_for_selector(page, selector)

    ctx = get_context_for_selector(page, selector)

    if ctx is None:
        raise RuntimeError(
            f"Selector not found for press_enter: {selector}"
        )

    ctx.press(selector, "Enter")


# ============================================================
# INPUT HELPERS
# ============================================================


def fill_input(page: Page, selector: str, value: str) -> None:
    """
    Generic input handler (frame-aware).
    """
    clear_and_fill(page, selector, value)


def click_and_fill(page: Page, selector: str, value: str) -> None:
    """
    Click into field then fill (useful for PeopleSoft focus behavior).
    """
    click(page, selector)
    fill(page, selector, value)


# ============================================================
# DATE HANDLING
# ============================================================


def get_current_date_mmddyyyy() -> str:
    return datetime.now().strftime("%m/%d/%Y")


def fill_current_date(page: Page, selector: str) -> None:
    date_str = get_current_date_mmddyyyy()
    fill_input(page, selector, date_str)


# ============================================================
# BUTTON ACTIONS
# ============================================================


def click_button(page: Page, selector: str) -> None:
    click(page, selector)


def set_checkbox_checked(
    page: Page,
    selector: str,
    checked: bool,
) -> None:
    """Set checkbox state (frame-aware)."""
    wait_for_selector(page, selector)

    ctx = get_context_for_selector(page, selector)

    if ctx is None:
        raise RuntimeError(
            f"Selector not found for set_checkbox_checked: {selector}"
        )

    ctx.locator(selector).set_checked(checked)


def submit(page: Page, selector: str) -> None:
    click_button(page, selector)


# ============================================================
# MODAL HANDLING
# ============================================================


def wait_for_modal(page: Page, selector: str = "div[role='dialog']") -> None:
    wait_for_selector(page, selector)


def close_modal(page: Page, selector: str) -> None:
    click_button(page, selector)


def click_button_if_present(
    page: Page,
    selector: str,
    timeout_ms: int = 5_000,
) -> bool:
    """
    Click selector when it appears; no-op if absent within timeout.
    Returns True if clicked.
    """

    deadline = time.monotonic() + (timeout_ms / 1000)

    while time.monotonic() < deadline:

        ctx = get_context_for_selector(page, selector)

        if ctx is not None:

            try:
                ctx.click(selector)
                wait_for_page_load(page)
                return True
            except Exception:
                pass

        page.wait_for_timeout(200)

    return False


def click_ok_if_present(
    page: Page,
    timeout_ms: int = 5_000,
) -> bool:
    """
    Click #ICOK when a message modal is shown; no-op if absent.
    Returns True if clicked.
    """

    return click_button_if_present(
        page,
        c.OK_BUTTON_SELECTOR,
        timeout_ms=timeout_ms,
    )


def dismiss_message_modals(
    page: Page,
    *,
    max_attempts: int = 5,
    delay_ms: int = 300,
) -> int:
    """
    Dismiss stacked PeopleSoft message modals (#ICOK).
    Returns how many OK clicks were performed.
    """
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
    """
    Click UNT privacy/terms Accept when the cookie modal is shown.
    Returns True if clicked.
    """

    page.wait_for_timeout(c.TERMS_MODAL_APPEAR_DELAY_MS)

    return click_button_if_present(
        page,
        c.TERMS_ACCEPT_BUTTON_SELECTOR,
        timeout_ms=timeout_ms,
    )


# ============================================================
# LOOKUP WORKFLOW PRIMITIVES
# ============================================================


def normalize_lookup_text(value: str) -> str:
    """Collapse whitespace for PeopleSoft lookup link vs input comparison."""
    return " ".join(str(value).split()).strip()


def format_location_for_lookup(value: str) -> str:
    """
    PeopleSoft location lookup expects building + two spaces + room.
    Display fields often render a single space; reconciliation CSVs use two.
    """
    text = str(value).replace("\u00a0", " ")
    collapsed = normalize_lookup_text(text)
    building, _, room = collapsed.partition(" ")
    if room:
        return f"{building}  {room}"
    return collapsed


def _text_matches_lookup(link_text: str, expected: str) -> bool:

    normalized_link = normalize_lookup_text(link_text)
    normalized_expected = normalize_lookup_text(expected)

    if normalized_link == normalized_expected:
        return True

    compact_link = normalized_link.replace(" ", "")
    compact_expected = normalized_expected.replace(" ", "")

    return compact_link == compact_expected


def _frame_has_selector(frame: Frame, selector: str) -> bool:

    try:
        return frame.query_selector(selector) is not None
    except Exception:
        return False


def _is_ptmod_frame(frame: Frame) -> bool:
    return "ptModFrame" in (frame.name or "") or "ptModFrame" in (
        frame.url or ""
    )


def is_open_lookup_modal_frame(frame: Frame) -> bool:
    """Shared updater helper for active PeopleSoft lookup modal frames."""
    if not _is_ptmod_frame(frame):
        return False

    return _frame_has_selector(
        frame,
        c.LOCATION_CODE_INPUT_SELECTOR,
    ) or _frame_has_selector(frame, c.EMPLOYEE_ID_INPUT_SELECTOR)


def get_lookup_modal_frame(
    page: Page,
    anchor_selector: str,
    timeout_ms: int = 30_000,
) -> Frame:
    """Frame that contains the active PeopleSoft lookup modal input."""
    deadline = time.monotonic() + (timeout_ms / 1000)

    while time.monotonic() < deadline:

        modal_matches: list[Frame] = []
        other_matches: list[Frame] = []

        for frame in page.frames:

            if not _frame_has_selector(frame, anchor_selector):
                continue

            if _is_ptmod_frame(frame):
                modal_matches.append(frame)
            else:
                other_matches.append(frame)

        if modal_matches:
            return modal_matches[0]

        if other_matches:
            return other_matches[0]

        page.wait_for_timeout(200)

    raise RuntimeError(
        f"Lookup modal frame not found (anchor: {anchor_selector})"
    )


def wait_for_modal_lookup_settled(
    frame: Frame,
    result_selector: str,
    timeout_ms: int = 15_000,
) -> None:
    """Wait for lookup results in the modal without networkidle."""
    frame.wait_for_selector(result_selector, timeout=timeout_ms)
    frame.wait_for_load_state("domcontentloaded", timeout=timeout_ms)


def wait_for_lookup_modal_closed(
    page: Page,
    anchor_selector: str,
    timeout_ms: int = 15_000,
) -> None:
    """Wait until the lookup modal iframe no longer exposes the anchor input."""
    deadline = time.monotonic() + (timeout_ms / 1000)

    while time.monotonic() < deadline:

        modal_open = False

        for frame in page.frames:

            if _is_ptmod_frame(frame) and _frame_has_selector(
                frame,
                anchor_selector,
            ):
                modal_open = True
                break

        if not modal_open:
            return

        page.wait_for_timeout(200)

    raise RuntimeError(
        f"Lookup modal did not close within {timeout_ms}ms "
        f"(anchor: {anchor_selector})"
    )


def fill_in_frame(frame: Frame, selector: str, value: str) -> None:
    frame.wait_for_selector(selector, timeout=30_000)
    frame.fill(selector, "")
    frame.fill(selector, value)


def click_in_frame(frame: Frame, selector: str) -> None:
    frame.wait_for_selector(selector, timeout=30_000)
    frame.click(selector)


def wait_for_lookup_results_in_frame(
    frame: Frame,
    result_selector: str,
    match_text: str,
    timeout_ms: int = 30_000,
) -> None:
    """Wait until a RESULT link in the modal matches the expected lookup text."""
    deadline = time.monotonic() + (timeout_ms / 1000)

    while time.monotonic() < deadline:

        locator = frame.locator(result_selector)

        try:

            for index in range(locator.count()):
                link_text = locator.nth(index).inner_text(timeout=2_000)

                if _text_matches_lookup(link_text, match_text):
                    return

        except Exception:
            pass

        frame.wait_for_timeout(200)

    candidates = _collect_lookup_link_texts_in_context(
        frame,
        result_selector,
    )

    raise RuntimeError(
        "Timed out waiting for lookup result "
        f"{match_text!r} "
        f"(expected {normalize_lookup_text(match_text)!r}). "
        f"Candidates in modal: {[repr(label) for label in candidates]}"
    )


def _collect_lookup_link_texts_in_context(
    context: Frame | Page,
    result_selector: str,
) -> list[str]:

    labels: list[str] = []

    try:
        locator = context.locator(result_selector)

        for index in range(locator.count()):
            labels.append(
                normalize_lookup_text(
                    locator.nth(index).inner_text(timeout=2_000),
                ),
            )

    except Exception:
        pass

    return labels


def _iter_lookup_contexts(page: Page, result_selector: str):

    with_results: list[Frame] = []
    with_lookup_input: list[Frame] = []
    modal_frames: list[Frame] = []
    other_frames: list[Frame] = []

    for frame in page.frames:

        try:

            if _frame_has_selector(frame, result_selector):
                with_results.append(frame)
            elif (
                _frame_has_selector(frame, c.LOCATION_CODE_INPUT_SELECTOR)
                or _frame_has_selector(frame, c.EMPLOYEE_ID_INPUT_SELECTOR)
            ):
                with_lookup_input.append(frame)
            elif _is_ptmod_frame(frame):
                modal_frames.append(frame)
            else:
                other_frames.append(frame)

        except Exception:
            other_frames.append(frame)

    yield from with_results
    yield from with_lookup_input
    yield from modal_frames
    yield page
    yield from other_frames


def _lookup_result_locators(
    page: Page,
    result_selector: str,
) -> list[tuple[Frame | Page, Locator]]:

    locators: list[tuple[Frame | Page, Locator]] = []

    for ctx in _iter_lookup_contexts(page, result_selector):

        try:
            locator = ctx.locator(result_selector)
            if locator.count() > 0:
                locators.append((ctx, locator))
        except Exception:
            continue

    return locators


def _click_lookup_link(link: Locator) -> None:
    """PeopleSoft result links use javascript:doUpdateParent via href."""
    link.scroll_into_view_if_needed()
    link.evaluate(
        """(el) => {
            const href = (el.getAttribute('href') || '').trim();
            if (href.startsWith('javascript:')) {
                const fn = href.slice('javascript:'.length).replace(/;\\s*$/, '');
                eval(fn);
                return;
            }
            el.click();
        }"""
    )


def _collect_lookup_link_texts(
    page: Page,
    result_selector: str,
) -> list[str]:

    labels: list[str] = []

    for _, locator in _lookup_result_locators(page, result_selector):

        try:

            for index in range(locator.count()):
                labels.append(
                    normalize_lookup_text(
                        locator.nth(index).inner_text(timeout=2_000),
                    ),
                )

        except Exception:
            continue

    return labels


def _click_first_lookup_result(page: Page, result_selector: str) -> None:

    for _, locator in _lookup_result_locators(page, result_selector):
        _click_lookup_link(locator.first)
        wait_for_page_load(page)
        return

    wait_for_selector(page, result_selector)
    click(page, result_selector)
    wait_for_page_load(page)


def open_lookup(page: Page, spyglass_selector: str) -> None:
    click(page, spyglass_selector)
    wait_for_page_load(page)


def search_lookup(
    page: Page,
    input_selector: str,
    value: str,
    search_button_selector: str,
) -> None:
    fill_input(page, input_selector, value)
    click(page, search_button_selector)
    wait_for_page_load(page)


def _select_lookup_result_in_context(
    context: Frame | Page,
    result_selector: str,
    match_text: str | None,
) -> None:

    locator = context.locator(result_selector)
    result_count = locator.count()

    if match_text is None:

        if result_count == 0:
            raise RuntimeError(
                f"No lookup results found for selector: {result_selector}"
            )

        _click_lookup_link(locator.first)
        return

    if result_count == 1:
        _click_lookup_link(locator.first)
        return

    for index in range(result_count):
        link = locator.nth(index)
        link_text = link.inner_text(timeout=2_000)

        if not _text_matches_lookup(link_text, match_text):
            continue

        _click_lookup_link(link)
        return

    candidates = _collect_lookup_link_texts_in_context(
        context,
        result_selector,
    )

    hint = ""
    if len(candidates) > 20:
        hint = (
            " Modal may be unfiltered; ensure search ran in this session."
        )

    raise RuntimeError(
        "No lookup result matched "
        f"{match_text!r} "
        f"(expected {normalize_lookup_text(match_text)!r}). "
        f"Candidates in modal: {[repr(label) for label in candidates]}."
        f"{hint}"
    )


def select_lookup_result(
    page: Page,
    result_selector: str,
    match_text: str | None = None,
    *,
    context: Frame | None = None,
    modal_anchor_selector: str | None = None,
) -> None:

    if context is not None:
        _select_lookup_result_in_context(
            context,
            result_selector,
            match_text,
        )
        if modal_anchor_selector:
            wait_for_lookup_modal_closed(
                page,
                modal_anchor_selector,
            )
        else:
            page.wait_for_timeout(500)
        return

    if match_text is None:
        _click_first_lookup_result(page, result_selector)
        return

    deadline = time.monotonic() + 30.0
    last_candidates: list[str] = []

    while time.monotonic() < deadline:

        for _, locator in _lookup_result_locators(page, result_selector):

            try:

                for index in range(locator.count()):
                    link = locator.nth(index)
                    link_text = link.inner_text(timeout=2_000)

                    if not _text_matches_lookup(link_text, match_text):
                        continue

                    _click_lookup_link(link)
                    wait_for_page_load(page)
                    return

            except Exception:
                continue

        last_candidates = _collect_lookup_link_texts(
            page,
            result_selector,
        )
        page.wait_for_timeout(300)

    hint = ""
    if len(last_candidates) > 20:
        hint = (
            " Modal may be unfiltered; ensure search ran in this session."
        )

    raise RuntimeError(
        "No lookup result matched "
        f"{match_text!r} "
        f"(expected {normalize_lookup_text(match_text)!r}). "
        f"Candidates: {[repr(label) for label in last_candidates]}."
        f"{hint}"
    )


# ============================================================
# PAGE STATE ACTIONS
# ============================================================


def get_display_text(
    page: Page,
    selector: str,
    *,
    normalize_whitespace: bool = True,
    timeout_ms: int = 30_000,
) -> str:
    """Read display-only span text (frame-aware)."""
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


def clear_field(page: Page, selector: str) -> None:

    ctx = get_context_for_selector(page, selector)

    if ctx is None:
        wait_for_selector(page, selector)
        ctx = get_context_for_selector(page, selector)

    if ctx is None:
        raise RuntimeError(
            f"Selector not found for clear_field: {selector}"
        )

    ctx.fill(selector, "")


def reset_and_search(
    page: Page,
    asset_id_selector: str,
    search_button_selector: str,
) -> None:
    clear_field(page, asset_id_selector)
    click_button(page, search_button_selector)
    wait_for_page_load(page)


# ============================================================
# SAFE WAIT WRAPPER
# ============================================================


def safe_wait(page: Page, ms: int = 1000) -> None:
    page.wait_for_timeout(ms)


# ============================================================
# COMPOSITE ACTIONS (STILL LEVEL_0 SAFE)
# ============================================================


def fill_business_unit(page: Page, selector: str, value: str) -> None:
    fill_input(page, selector, value)


def fill_tag_number(page: Page, selector: str, value: str) -> None:
    fill_input(page, selector, value)


def fill_asset_id(page: Page, selector: str, value: str) -> None:
    fill_input(page, selector, value)


# ============================================================
# DIAGNOSTICS & PAGE STATE
# ============================================================


def get_page_url(page: Page) -> str:
    """Return current page URL."""
    return page.url


def get_page_title(page: Page) -> str:
    """Return current page title."""
    return page.title()


def log_page_state(page: Page, prefix: str = "") -> None:
    """Log page URL and title for debugging."""
    url = get_page_url(page)
    title = get_page_title(page)
    log_and_print(f"{prefix} URL: {url}")
    log_and_print(f"{prefix} Title: {title}")


def selector_exists(page: Page, selector: str) -> bool:
    """Check if selector exists on page or in any frame."""
    return get_context_for_selector(page, selector) is not None


def wait_for_url_contains(
    page: Page,
    substring: str,
    timeout_ms: int = 30_000,
) -> None:
    """Wait for page URL to contain substring (useful post-redirect)."""
    page.wait_for_url(f"**/*{substring}*", timeout=timeout_ms)


def wait_for_selector_with_diagnostics(
    page: Page,
    selector: str,
    timeout_ms: int = 100_000,
) -> None:
    """
    Wait for selector with enhanced diagnostics.
    Logs page state before and after failure.
    """
    try:
        wait_for_selector(page, selector, timeout_ms)
    except Exception as e:
        log_and_print(f"\n[DIAGNOSTIC] Selector wait failed: {selector}")
        log_page_state(page, "[DIAGNOSTIC]")
        log_and_print(
            f"[DIAGNOSTIC] Selector exists: "
            f"{selector_exists(page, selector)}"
        )
        log_and_print(f"[DIAGNOSTIC] Error: {e}\n")
        raise


def click_ctx(page: Page, selector: str) -> None:
    ctx = get_active_frame(page)
    ctx.click(selector)


def fill_ctx(page: Page, selector: str, value: str) -> None:
    ctx = get_active_frame(page)
    ctx.fill(selector, value)


def wait_for_selector_ctx(
    page: Page,
    selector: str,
    timeout_ms: int = 100_000,
) -> None:
    ctx = get_active_frame(page)
    ctx.wait_for_selector(selector, timeout=timeout_ms)
