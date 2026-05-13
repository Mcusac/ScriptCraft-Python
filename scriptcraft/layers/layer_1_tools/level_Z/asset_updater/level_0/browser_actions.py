# ============================================================
# browser_actions.py — LEVEL_0 BROWSER PRIMITIVES
#
# PURPOSE:
# - Low-level browser interaction only
# - No business logic
# - No data transformations
# - No workflow assumptions
#
# DESIGN:
# - Composable atomic actions
# - Reusable across pages/modals
# - Playwright-first patterns
# ============================================================

from datetime import datetime
from playwright.sync_api import Page


# ============================================================
# NAVIGATION
# ============================================================

def navigate(page: Page, url: str) -> None:
    page.goto(url)


def wait_for_page_load(page: Page, timeout_ms: int = 100_000) -> None:
    page.wait_for_load_state("networkidle", timeout=timeout_ms)


def wait_for_selector(page: Page, selector: str, timeout_ms: int = 100_000) -> None:
    page.wait_for_selector(selector, timeout=timeout_ms)


# ============================================================
# BASIC INTERACTIONS
# ============================================================

def click(page: Page, selector: str) -> None:
    page.click(selector)


def fill(page: Page, selector: str, value: str) -> None:
    page.fill(selector, value)


def clear_and_fill(page: Page, selector: str, value: str) -> None:
    page.fill(selector, "")
    page.fill(selector, value)


def press_enter(page: Page, selector: str) -> None:
    page.press(selector, "Enter")


# ============================================================
# INPUT HELPERS
# ============================================================

def fill_input(page: Page, selector: str, value: str) -> None:
    """
    Generic input handler (safe default abstraction).
    """
    wait_for_selector(page, selector)
    clear_and_fill(page, selector, value)


def click_and_fill(page: Page, selector: str, value: str) -> None:
    """
    Click into field then fill (useful for PeopleSoft focus behavior).
    """
    click(page, selector)
    fill(page, selector, value)


# ============================================================
# DATE HANDLING
# ============================================================

def get_current_date_mmddyyyy() -> str:
    return datetime.now().strftime("%m/%d/%Y")


def fill_current_date(page: Page, selector: str) -> None:
    date_str = get_current_date_mmddyyyy()
    fill_input(page, selector, date_str)


# ============================================================
# BUTTON ACTIONS
# ============================================================

def click_button(page: Page, selector: str) -> None:
    wait_for_selector(page, selector)
    click(page, selector)


def submit(page: Page, selector: str) -> None:
    click_button(page, selector)


# ============================================================
# MODAL HANDLING
# ============================================================

def wait_for_modal(page: Page, selector: str = "div[role='dialog']") -> None:
    wait_for_selector(page, selector)


def close_modal(page: Page, selector: str) -> None:
    click_button(page, selector)


# ============================================================
# LOOKUP WORKFLOW PRIMITIVES
# ============================================================

def open_lookup(page: Page, spyglass_selector: str) -> None:
    click(page, spyglass_selector)
    wait_for_page_load(page)


def search_lookup(page: Page, input_selector: str, value: str, search_button_selector: str) -> None:
    fill_input(page, input_selector, value)
    click(page, search_button_selector)
    wait_for_page_load(page)


def select_lookup_result(page: Page, result_selector: str) -> None:
    wait_for_selector(page, result_selector)
    click(page, result_selector)
    wait_for_page_load(page)


# ============================================================
# PAGE STATE ACTIONS
# ============================================================

def clear_field(page: Page, selector: str) -> None:
    page.fill(selector, "")


def reset_and_search(page: Page, asset_id_selector: str, search_button_selector: str) -> None:
    clear_field(page, asset_id_selector)
    click_button(page, search_button_selector)
    wait_for_page_load(page)


# ============================================================
# SAFE WAIT WRAPPER
# ============================================================

def safe_wait(page: Page, ms: int = 1000) -> None:
    page.wait_for_timeout(ms)


# ============================================================
# COMPOSITE ACTIONS (STILL LEVEL_0 SAFE)
# ============================================================

def fill_business_unit(page: Page, selector: str, value: str) -> None:
    fill_input(page, selector, value)


def fill_tag_number(page: Page, selector: str, value: str) -> None:
    fill_input(page, selector, value)


def fill_asset_id(page: Page, selector: str, value: str) -> None:
    fill_input(page, selector, value)