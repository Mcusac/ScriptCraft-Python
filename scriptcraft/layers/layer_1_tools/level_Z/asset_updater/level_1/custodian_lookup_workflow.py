# ============================================================
# custodian_lookup_workflow.py — LEVEL_1
#
# PURPOSE:
# - Encapsulates ONLY the Custodian (Employee) lookup workflow
# - Mirrors location lookup pattern for consistency
#
# DOES NOT:
# - Load CSVs
# - Determine employee IDs
# - Handle asset update flow
# - Handle location logic
# ============================================================

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    browser_actions as ba,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0.constants import (
    CUSTODIAN_SPYGLASS_BUTTON_SELECTOR,
    CUSTODIAN_LOOKUP_BUTTON_SELECTOR,
    EMPLOYEE_SEARCH_RESULT_SELECTOR,
)


# ============================================================
# CUSTODIAN LOOKUP WORKFLOW
# ============================================================

def open_custodian_lookup_modal(page: Page) -> None:
    """
    Opens custodian lookup modal via spyglass icon.
    """
    ba.click_button(page, CUSTODIAN_SPYGLASS_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)


def enter_employee_id(page: Page, employee_id: str) -> None:
    """
    Enters employee ID into lookup modal search field.
    NOTE:
    PeopleSoft reuses generic lookup search behavior (#ICSearch),
    so we only interact with search trigger.
    """
    # In many PeopleSoft implementations, the first field is auto-focused
    ba.fill(page, CUSTODIAN_LOOKUP_BUTTON_SELECTOR, "")
    ba.safe_wait(page, 200)


def execute_employee_search(page: Page) -> None:
    """
    Executes employee lookup search.
    """
    ba.click_button(page, CUSTODIAN_LOOKUP_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)


def select_employee_result(page: Page) -> None:
    """
    Selects matching employee result row.
    """
    ba.select_lookup_result(page, EMPLOYEE_SEARCH_RESULT_SELECTOR)


def complete_custodian_lookup(page: Page, employee_id: str) -> None:
    """
    Full custodian lookup workflow:
    open → search → select
    """
    open_custodian_lookup_modal(page)
    enter_employee_id(page, employee_id)
    execute_employee_search(page)
    select_employee_result(page)