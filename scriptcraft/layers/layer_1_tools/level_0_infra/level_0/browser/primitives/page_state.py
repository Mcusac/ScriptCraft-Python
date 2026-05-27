"""Read page URL/title (Playwright Page only)."""

from playwright.sync_api import Page


def get_page_url(page: Page) -> str:
    return page.url


def get_page_title(page: Page) -> str:
    return page.title()
