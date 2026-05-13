# asset_search_step.py — LEVEL_1

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    browser_actions as ba,
    constants as c,
)


def execute_asset_search_step(page: Page, tag_number: str) -> None:
    """
    Executes ONLY asset search step.
    """

    ba.fill(page, c.TAG_NUMBER_INPUT_SELECTOR, tag_number)
    ba.click(page, c.SEARCH_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)