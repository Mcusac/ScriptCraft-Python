"""Thin selector-driven fill aliases (same behavior, named for call sites)."""

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.composed.input_flow import (
    fill_input,
)


def fill_business_unit(page: Page, selector: str, value: str) -> None:
    fill_input(page, selector, value)


def fill_tag_number(page: Page, selector: str, value: str) -> None:
    fill_input(page, selector, value)


def fill_asset_id(page: Page, selector: str, value: str) -> None:
    fill_input(page, selector, value)
