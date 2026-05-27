"""Lookup modal result selection (selector-driven; no tool constants)."""

import time
from collections.abc import Iterator, Sequence

from playwright.sync_api import Frame, Locator, Page

from scriptcraft.layers.layer_0_core.level_0 import poll_until_deadline

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.composed.frame_interact import (
    click,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.composed.frame_wait import (
    wait_for_selector,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.composed.input_flow import (
    fill_input,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.frame.modal_poll import (
    wait_for_lookup_modal_closed,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.frame.probe import (
    frame_has_selector,
    is_ptmod_frame,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.lookup_text import (
    normalize_lookup_text,
    text_matches_lookup,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.primitives.navigation import (
    wait_for_page_load,
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


def _iter_lookup_contexts(
    page: Page,
    result_selector: str,
    lookup_input_selectors: Sequence[str],
) -> Iterator[Frame | Page]:
    with_results: list[Frame] = []
    with_lookup_input: list[Frame] = []
    modal_frames: list[Frame] = []
    other_frames: list[Frame] = []

    for frame in page.frames:
        try:
            if frame_has_selector(frame, result_selector):
                with_results.append(frame)
            elif any(
                frame_has_selector(frame, sel) for sel in lookup_input_selectors
            ):
                with_lookup_input.append(frame)
            elif is_ptmod_frame(frame):
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
    lookup_input_selectors: Sequence[str],
) -> list[tuple[Frame | Page, Locator]]:
    locators: list[tuple[Frame | Page, Locator]] = []
    for ctx in _iter_lookup_contexts(
        page,
        result_selector,
        lookup_input_selectors,
    ):
        try:
            locator = ctx.locator(result_selector)
            if locator.count() > 0:
                locators.append((ctx, locator))
        except Exception:
            continue
    return locators


def _click_lookup_link(link: Locator) -> None:
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


def wait_for_lookup_results_in_frame(
    frame: Frame,
    result_selector: str,
    match_text: str,
    timeout_ms: int = 30_000,
) -> None:
    def _result_visible() -> bool:
        locator = frame.locator(result_selector)
        try:
            for index in range(locator.count()):
                link_text = locator.nth(index).inner_text(timeout=2_000)
                if text_matches_lookup(link_text, match_text):
                    return True
        except Exception:
            pass
        return False

    if poll_until_deadline(
        _result_visible,
        timeout_ms=timeout_ms,
        poll_ms=200,
        on_poll=frame.page.wait_for_timeout,
    ):
        return

    candidates = _collect_lookup_link_texts_in_context(frame, result_selector)
    raise RuntimeError(
        "Timed out waiting for lookup result "
        f"{match_text!r} "
        f"(expected {normalize_lookup_text(match_text)!r}). "
        f"Candidates in modal: {[repr(label) for label in candidates]}"
    )


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
        if not text_matches_lookup(link_text, match_text):
            continue
        _click_lookup_link(link)
        return

    candidates = _collect_lookup_link_texts_in_context(context, result_selector)
    hint = ""
    if len(candidates) > 20:
        hint = " Modal may be unfiltered; ensure search ran in this session."
    raise RuntimeError(
        "No lookup result matched "
        f"{match_text!r} "
        f"(expected {normalize_lookup_text(match_text)!r}). "
        f"Candidates in modal: {[repr(label) for label in candidates]}."
        f"{hint}"
    )


def _collect_lookup_link_texts(
    page: Page,
    result_selector: str,
    lookup_input_selectors: Sequence[str],
) -> list[str]:
    labels: list[str] = []
    for _, locator in _lookup_result_locators(
        page,
        result_selector,
        lookup_input_selectors,
    ):
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


def _click_first_lookup_result(
    page: Page,
    result_selector: str,
    lookup_input_selectors: Sequence[str],
) -> None:
    for _, locator in _lookup_result_locators(
        page,
        result_selector,
        lookup_input_selectors,
    ):
        _click_lookup_link(locator.first)
        wait_for_page_load(page)
        return

    wait_for_selector(page, result_selector)
    click(page, result_selector)
    wait_for_page_load(page)


def select_lookup_result(
    page: Page,
    result_selector: str,
    match_text: str | None = None,
    *,
    context: Frame | None = None,
    modal_anchor_selector: str | None = None,
    lookup_input_selectors: Sequence[str] = (),
) -> None:
    if context is not None:
        _select_lookup_result_in_context(context, result_selector, match_text)
        if modal_anchor_selector:
            wait_for_lookup_modal_closed(page, modal_anchor_selector)
        else:
            page.wait_for_timeout(500)
        return

    if match_text is None:
        _click_first_lookup_result(
            page,
            result_selector,
            lookup_input_selectors,
        )
        return

    deadline = time.monotonic() + 30.0
    last_candidates: list[str] = []

    while time.monotonic() < deadline:
        for _, locator in _lookup_result_locators(
            page,
            result_selector,
            lookup_input_selectors,
        ):
            try:
                for index in range(locator.count()):
                    link = locator.nth(index)
                    link_text = link.inner_text(timeout=2_000)
                    if not text_matches_lookup(link_text, match_text):
                        continue
                    _click_lookup_link(link)
                    wait_for_page_load(page)
                    return
            except Exception:
                continue

        last_candidates = _collect_lookup_link_texts(
            page,
            result_selector,
            lookup_input_selectors,
        )
        page.wait_for_timeout(300)

    hint = ""
    if len(last_candidates) > 20:
        hint = " Modal may be unfiltered; ensure search ran in this session."
    raise RuntimeError(
        "No lookup result matched "
        f"{match_text!r} "
        f"(expected {normalize_lookup_text(match_text)!r}). "
        f"Candidates: {[repr(label) for label in last_candidates]}."
        f"{hint}"
    )
