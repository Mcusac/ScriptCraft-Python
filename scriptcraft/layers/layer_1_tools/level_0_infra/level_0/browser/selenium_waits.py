"""Selenium wait primitives (URL-based, no DOM assumptions)."""

import time

from typing import Any


def wait_until_url_excludes(
    driver: Any,
    substring: str,
    *,
    timeout_s: int,
) -> bool:
    """
    Poll until ``substring`` is absent from the current URL (case-insensitive).

    Returns True if the condition is met before timeout, False otherwise.
    """
    needle = substring.lower()
    start = time.time()
    while needle in (driver.current_url or "").lower() and (time.time() - start) < timeout_s:
        time.sleep(1)
    return needle not in (driver.current_url or "").lower()
