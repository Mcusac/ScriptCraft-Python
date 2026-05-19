import time

from typing import Callable
from playwright.sync_api import Page


def poll_until(
    page: Page,
    condition: Callable[[], bool],
    *,
    timeout_ms: int,
    poll_ms: int,
) -> bool:
    """Shared updater polling helper with unchanged caller timing constants."""
    deadline = time.monotonic() + (timeout_ms / 1000)

    while time.monotonic() < deadline:
        if condition():
            return True
        page.wait_for_timeout(poll_ms)

    return False
