# asset_update_step.py — LEVEL_2

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
    constants as c,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    complete_location_lookup,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    complete_custodian_lookup,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    read_current_employee_id,
    read_current_location_code,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    apply_offsite_and_authorization,
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

    ba.fill_current_date(page, c.DATE_OF_TRANSFER_INPUT_SELECTOR)

    if not location_code:
        location_code = read_current_location_code(page)

    if not employee_id:
        employee_id = read_current_employee_id(page)

    complete_location_lookup(page, location_code)
    complete_custodian_lookup(page, employee_id)

    apply_offsite_and_authorization(page, location_code)
