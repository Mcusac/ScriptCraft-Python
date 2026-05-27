"""Higher-level input sequences composed from frame interact + dates."""

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.composed.frame_interact import (
    clear_and_fill,
    click,
    fill,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.primitives.dates import (
    get_current_date_mmddyyyy,
)


def fill_input(page: Page, selector: str, value: str) -> None:
    clear_and_fill(page, selector, value)


def click_and_fill(page: Page, selector: str, value: str) -> None:
    click(page, selector)
    fill(page, selector, value)


def click_button(page: Page, selector: str) -> None:
    click(page, selector)


def submit(page: Page, selector: str) -> None:
    click_button(page, selector)


def fill_current_date(page: Page, selector: str) -> None:
    fill_input(page, selector, get_current_date_mmddyyyy())
