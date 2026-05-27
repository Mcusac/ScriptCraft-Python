"""Lazy Selenium browser launch (optional dependency)."""

from __future__ import annotations

from typing import Any


def launch_chrome(*, detach: bool = True) -> Any:
    """
    Launch a Chrome WebDriver instance.

    Selenium is imported lazily so this package does not require selenium until used.
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "selenium is required to launch the browser. Install it (e.g. `pip install selenium`)."
        ) from e

    options = Options()
    if detach:
        options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=options)
