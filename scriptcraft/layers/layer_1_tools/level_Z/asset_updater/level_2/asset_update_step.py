from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    browser_actions as ba,
    constants as c,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1.location_lookup_workflow import (
    complete_location_lookup,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1.custodian_lookup_workflow import (
    complete_custodian_lookup,
)


def execute_asset_update_step(
    page: Page,
    location_code: str,
    employee_id: str
) -> None:
    """
    Handles update section of workflow only.
    """

    # date
    ba.fill(page, c.DATE_OF_TRANSFER_SELECTOR, ba.current_date_mmddyyyy())

    # location
    complete_location_lookup(page, location_code)

    # custodian
    complete_custodian_lookup(page, employee_id)