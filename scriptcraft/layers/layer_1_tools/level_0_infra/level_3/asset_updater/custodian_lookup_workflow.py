from playwright.sync_api import Frame, Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    CUSTODIAN_LOOKUP_BUTTON_SELECTOR,
    CUSTODIAN_SPYGLASS_BUTTON_SELECTOR,
    EMPLOYEE_ID_INPUT_SELECTOR,
    EMPLOYEE_SEARCH_RESULT_SELECTOR,
    click_button,
    click_in_frame,
    fill_in_frame,
    get_lookup_modal_frame,
    wait_for_modal_lookup_settled,
    wait_for_page_load,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    select_lookup_result,
    wait_for_lookup_results_in_frame,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    complete_modal_lookup,
)


def open_custodian_lookup_modal(page: Page) -> None:
    click_button(page, CUSTODIAN_SPYGLASS_BUTTON_SELECTOR)
    wait_for_page_load(page)


def get_custodian_lookup_frame(page: Page) -> Frame:
    return get_lookup_modal_frame(page, EMPLOYEE_ID_INPUT_SELECTOR)


def execute_employee_search_in_frame(frame: Frame) -> None:
    click_in_frame(frame, CUSTODIAN_LOOKUP_BUTTON_SELECTOR)
    wait_for_modal_lookup_settled(
        frame,
        EMPLOYEE_SEARCH_RESULT_SELECTOR,
    )


def select_employee_result_in_frame(
    page: Page,
    frame: Frame,
    employee_id: str,
) -> None:
    wait_for_lookup_results_in_frame(
        frame,
        EMPLOYEE_SEARCH_RESULT_SELECTOR,
        employee_id,
    )
    select_lookup_result(
        page,
        EMPLOYEE_SEARCH_RESULT_SELECTOR,
        match_text=employee_id,
        context=frame,
        modal_anchor_selector=EMPLOYEE_ID_INPUT_SELECTOR,
    )


def enter_employee_id(page: Page, employee_id: str) -> None:
    frame = get_custodian_lookup_frame(page)
    fill_in_frame(frame, EMPLOYEE_ID_INPUT_SELECTOR, employee_id)


def execute_employee_search(page: Page) -> None:
    frame = get_custodian_lookup_frame(page)
    execute_employee_search_in_frame(frame)


def select_employee_result(page: Page, employee_id: str) -> None:
    frame = get_custodian_lookup_frame(page)
    select_employee_result_in_frame(page, frame, employee_id)


def complete_custodian_lookup(page: Page, employee_id: str) -> None:
    complete_modal_lookup(
        page,
        spyglass_selector=CUSTODIAN_SPYGLASS_BUTTON_SELECTOR,
        anchor_selector=EMPLOYEE_ID_INPUT_SELECTOR,
        code_input_selector=EMPLOYEE_ID_INPUT_SELECTOR,
        search_button_selector=CUSTODIAN_LOOKUP_BUTTON_SELECTOR,
        result_selector=EMPLOYEE_SEARCH_RESULT_SELECTOR,
        value=employee_id,
    )

