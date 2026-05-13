# asset_post_update_step.py — LEVEL_1

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    browser_actions as ba,
    constants as c,
)


def execute_asset_post_update_step(page: Page) -> None:
    """
    Handles submission + cleanup flow.
    """

    ba.click_button(page, c.UPDATE_THIS_ASSET_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)

    ba.click_button(page, c.OK_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)

    ba.click_button(page, c.RETURN_TO_SEARCH_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)