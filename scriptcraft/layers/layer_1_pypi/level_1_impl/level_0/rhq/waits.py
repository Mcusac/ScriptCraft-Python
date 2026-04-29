"""
Wait helpers for RHQ Selenium flows.
"""

import time

from typing import Any


def wait_until_not_on_login(driver: Any, *, timeout_s: int) -> bool:
    """
    Wait until the current URL no longer contains 'login' (case-insensitive).
    Returns True if the condition is met before timeout, False otherwise.
    """
    start = time.time()
    while "login" in (driver.current_url or "").lower() and (time.time() - start) < timeout_s:
        time.sleep(1)
    return "login" not in (driver.current_url or "").lower()

