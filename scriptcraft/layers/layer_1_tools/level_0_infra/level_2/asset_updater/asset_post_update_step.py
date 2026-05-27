# asset_post_update_step.py — LEVEL_2

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    OK_BUTTON_SELECTOR,
    RETURN_TO_SEARCH_BUTTON_SELECTOR,
    UPDATE_THIS_ASSET_BUTTON_SELECTOR,
    wait_for_page_load,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import click_button


def execute_asset_post_update_step(page: Page) -> None:
    """
    Handles submission + cleanup flow.
    """

    click_button(page, UPDATE_THIS_ASSET_BUTTON_SELECTOR)
    wait_for_page_load(page)

    click_button(page, OK_BUTTON_SELECTOR)
    wait_for_page_load(page)

    click_button(page, RETURN_TO_SEARCH_BUTTON_SELECTOR)
    wait_for_page_load(page)

