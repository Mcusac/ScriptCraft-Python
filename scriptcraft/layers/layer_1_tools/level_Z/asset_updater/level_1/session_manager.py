# session_manager.py — LEVEL_1

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    browser_actions as ba,
    constants as c,
)


def open_asset_updater(page: Page, url: str) -> None:
    """
    Navigates to asset updater system.
    """
    ba.navigate(page, url)
    ba.wait_for_page_load(page)


def set_business_unit(page: Page) -> None:
    """
    Sets static business unit (HS763).
    """
    ba.fill_input(page, c.BUSINESS_UNIT_INPUT_SELECTOR, c.BUSINESS_UNIT_VALUE)
    ba.safe_wait(page, 1000)