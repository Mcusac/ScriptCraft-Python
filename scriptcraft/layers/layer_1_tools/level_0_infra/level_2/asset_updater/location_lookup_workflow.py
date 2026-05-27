from playwright.sync_api import Frame, Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    LOCATION_CODE_INPUT_SELECTOR,
    LOCATION_LOOKUP_BUTTON_SELECTOR,
    LOCATION_SEARCH_RESULT_SELECTOR,
    LOCATION_SPYGLASS_BUTTON_SELECTOR,
    click_button,
    click_in_frame,
    fill_in_frame,
    format_location_for_lookup,
    get_lookup_modal_frame,
    wait_for_modal_lookup_settled,
    wait_for_page_load,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    select_lookup_result,
    wait_for_lookup_results_in_frame,
)
from .lookup_modal_workflow import complete_modal_lookup


def open_location_lookup_modal(page: Page) -> None:
    click_button(page, LOCATION_SPYGLASS_BUTTON_SELECTOR)
    wait_for_page_load(page)


def get_location_lookup_frame(page: Page) -> Frame:
    return get_lookup_modal_frame(page, LOCATION_CODE_INPUT_SELECTOR)


def enter_location_code_in_frame(
    frame: Frame,
    location_code: str,
) -> None:
    formatted = format_location_for_lookup(location_code)
    fill_in_frame(frame, LOCATION_CODE_INPUT_SELECTOR, formatted)


def execute_location_search_in_frame(frame: Frame) -> None:
    click_in_frame(frame, LOCATION_LOOKUP_BUTTON_SELECTOR)
    wait_for_modal_lookup_settled(
        frame,
        LOCATION_SEARCH_RESULT_SELECTOR,
    )


def select_location_result_in_frame(
    page: Page,
    frame: Frame,
    location_code: str,
) -> None:
    formatted = format_location_for_lookup(location_code)
    wait_for_lookup_results_in_frame(
        frame,
        LOCATION_SEARCH_RESULT_SELECTOR,
        formatted,
    )
    select_lookup_result(
        page,
        LOCATION_SEARCH_RESULT_SELECTOR,
        match_text=formatted,
        context=frame,
        modal_anchor_selector=LOCATION_CODE_INPUT_SELECTOR,
    )


def enter_location_code(page: Page, location_code: str) -> None:
    frame = get_location_lookup_frame(page)
    enter_location_code_in_frame(frame, location_code)


def execute_location_search(page: Page) -> None:
    frame = get_location_lookup_frame(page)
    execute_location_search_in_frame(frame)


def select_location_result(page: Page, location_code: str) -> None:
    frame = get_location_lookup_frame(page)
    select_location_result_in_frame(page, frame, location_code)


def complete_location_lookup(page: Page, location_code: str) -> None:
    complete_modal_lookup(
        page,
        spyglass_selector=LOCATION_SPYGLASS_BUTTON_SELECTOR,
        anchor_selector=LOCATION_CODE_INPUT_SELECTOR,
        code_input_selector=LOCATION_CODE_INPUT_SELECTOR,
        search_button_selector=LOCATION_LOOKUP_BUTTON_SELECTOR,
        result_selector=LOCATION_SEARCH_RESULT_SELECTOR,
        value=location_code,
        format_value=format_location_for_lookup,
    )

