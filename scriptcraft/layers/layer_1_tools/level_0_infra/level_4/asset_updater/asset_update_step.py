# asset_update_step.py — LEVEL_3

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    DATE_OF_TRANSFER_INPUT_SELECTOR,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import fill_current_date
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import apply_offsite_and_authorization
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    complete_custodian_lookup,
    complete_location_lookup,
    read_current_employee_id,
    read_current_location_code,
)

def execute_asset_update_step(
    page: Page,
    location_code: str | None = None,
    employee_id: str | None = None,
) -> None:
    """
    Handles update section of workflow only.
    Missing CSV values are read from Current Asset Details on the page.
    """

    fill_current_date(page, DATE_OF_TRANSFER_INPUT_SELECTOR)

    if not location_code:
        location_code = read_current_location_code(page)

    if not employee_id:
        employee_id = read_current_employee_id(page)

    complete_location_lookup(page, location_code)
    complete_custodian_lookup(page, employee_id)

    apply_offsite_and_authorization(page, location_code)
