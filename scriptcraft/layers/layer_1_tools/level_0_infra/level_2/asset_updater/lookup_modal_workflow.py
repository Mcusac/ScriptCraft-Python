"""Shared PeopleSoft modal lookup orchestration (mechanism, not domain policy)."""

from collections.abc import Callable

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    click_button,
    click_in_frame,
    fill_in_frame,
    get_lookup_modal_frame,
    wait_for_lookup_results_in_frame,
    wait_for_modal_lookup_settled,
    wait_for_page_load,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    select_lookup_result,
)


def complete_modal_lookup(
    page: Page,
    *,
    spyglass_selector: str,
    anchor_selector: str,
    code_input_selector: str,
    search_button_selector: str,
    result_selector: str,
    value: str,
    format_value: Callable[[str], str] | None = None,
) -> None:
    """
    Open lookup modal, search, and select a row matching ``value``.

    ``format_value`` applies domain formatting before fill/search/match
    (e.g. location building/room spacing).
    """
    display_value = format_value(value) if format_value else value

    click_button(page, spyglass_selector)
    wait_for_page_load(page)

    frame = get_lookup_modal_frame(page, anchor_selector)
    fill_in_frame(frame, code_input_selector, display_value)
    click_in_frame(frame, search_button_selector)
    wait_for_modal_lookup_settled(frame, result_selector)

    frame = get_lookup_modal_frame(page, anchor_selector)
    wait_for_lookup_results_in_frame(
        frame,
        result_selector,
        display_value,
    )
    select_lookup_result(
        page,
        result_selector,
        match_text=display_value,
        context=frame,
        modal_anchor_selector=anchor_selector,
    )
