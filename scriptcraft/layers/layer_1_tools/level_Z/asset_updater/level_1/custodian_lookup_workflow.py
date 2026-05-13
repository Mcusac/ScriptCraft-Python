# custodian_lookup_workflow.py — LEVEL_1

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    browser_actions as ba,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0.constants import (
    CUSTODIAN_SPYGLASS_BUTTON_SELECTOR,
    EMPLOYEE_ID_INPUT_SELECTOR,
    CUSTODIAN_LOOKUP_BUTTON_SELECTOR,
    EMPLOYEE_SEARCH_RESULT_SELECTOR,
)


def open_custodian_lookup_modal(page: Page) -> None:
    ba.click_button(page, CUSTODIAN_SPYGLASS_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)


def enter_employee_id(page: Page, employee_id: str) -> None:
    ba.fill_input(page, EMPLOYEE_ID_INPUT_SELECTOR, employee_id)


def execute_employee_search(page: Page) -> None:
    ba.click_button(page, CUSTODIAN_LOOKUP_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)


def select_employee_result(page: Page) -> None:
    ba.select_lookup_result(page, EMPLOYEE_SEARCH_RESULT_SELECTOR)


def complete_custodian_lookup(page: Page, employee_id: str) -> None:
    open_custodian_lookup_modal(page)
    enter_employee_id(page, employee_id)
    execute_employee_search(page)
    select_employee_result(page)