# custodian_lookup_workflow.py — LEVEL_1

from playwright.sync_api import Frame, Page

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    CUSTODIAN_SPYGLASS_BUTTON_SELECTOR,
    EMPLOYEE_ID_INPUT_SELECTOR,
    CUSTODIAN_LOOKUP_BUTTON_SELECTOR,
    EMPLOYEE_SEARCH_RESULT_SELECTOR,
)


def open_custodian_lookup_modal(page: Page) -> None:
    ba.click_button(page, CUSTODIAN_SPYGLASS_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)


def get_custodian_lookup_frame(page: Page) -> Frame:
    return ba.get_lookup_modal_frame(page, EMPLOYEE_ID_INPUT_SELECTOR)


def execute_employee_search_in_frame(frame: Frame) -> None:
    ba.click_in_frame(frame, CUSTODIAN_LOOKUP_BUTTON_SELECTOR)
    ba.wait_for_modal_lookup_settled(
        frame,
        EMPLOYEE_SEARCH_RESULT_SELECTOR,
    )


def select_employee_result_in_frame(
    page: Page,
    frame: Frame,
    employee_id: str,
) -> None:
    ba.wait_for_lookup_results_in_frame(
        frame,
        EMPLOYEE_SEARCH_RESULT_SELECTOR,
        employee_id,
    )
    ba.select_lookup_result(
        page,
        EMPLOYEE_SEARCH_RESULT_SELECTOR,
        match_text=employee_id,
        context=frame,
        modal_anchor_selector=EMPLOYEE_ID_INPUT_SELECTOR,
    )


def enter_employee_id(page: Page, employee_id: str) -> None:
    frame = get_custodian_lookup_frame(page)
    ba.fill_in_frame(frame, EMPLOYEE_ID_INPUT_SELECTOR, employee_id)


def execute_employee_search(page: Page) -> None:
    frame = get_custodian_lookup_frame(page)
    execute_employee_search_in_frame(frame)


def select_employee_result(page: Page, employee_id: str) -> None:
    frame = get_custodian_lookup_frame(page)
    select_employee_result_in_frame(page, frame, employee_id)


def complete_custodian_lookup(page: Page, employee_id: str) -> None:
    open_custodian_lookup_modal(page)
    frame = get_custodian_lookup_frame(page)
    ba.fill_in_frame(frame, EMPLOYEE_ID_INPUT_SELECTOR, employee_id)
    execute_employee_search_in_frame(frame)
    frame = get_custodian_lookup_frame(page)
    select_employee_result_in_frame(page, frame, employee_id)
