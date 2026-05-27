"""Direct interactions inside a resolved Frame (Playwright only)."""

from playwright.sync_api import Frame


def wait_for_modal_lookup_settled(
    frame: Frame,
    result_selector: str,
    timeout_ms: int = 15_000,
) -> None:
    frame.wait_for_selector(result_selector, timeout=timeout_ms)
    frame.wait_for_load_state("domcontentloaded", timeout=timeout_ms)


def fill_in_frame(frame: Frame, selector: str, value: str) -> None:
    frame.wait_for_selector(selector, timeout=30_000)
    frame.fill(selector, "")
    frame.fill(selector, value)


def click_in_frame(frame: Frame, selector: str) -> None:
    frame.wait_for_selector(selector, timeout=30_000)
    frame.click(selector)
