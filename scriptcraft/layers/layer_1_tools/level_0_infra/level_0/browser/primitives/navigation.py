"""Page navigation and timing (Playwright Page only)."""

from playwright.sync_api import Page


def navigate(page: Page, url: str) -> None:
    page.goto(url)


def wait_for_page_load(page: Page, timeout_ms: int = 100_000) -> None:
    page.wait_for_load_state("networkidle", timeout=timeout_ms)


def safe_wait(page: Page, ms: int = 1000) -> None:
    page.wait_for_timeout(ms)


def wait_for_url_contains(
    page: Page,
    substring: str,
    timeout_ms: int = 30_000,
) -> None:
    page.wait_for_url(f"**/*{substring}*", timeout=timeout_ms)
