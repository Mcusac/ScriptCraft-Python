from __future__ import annotations

from typing import Any


def launch_browser() -> Any:
    """
    Launch a Chrome webdriver instance.

    Selenium is imported lazily so importing this package does not require selenium
    unless browser automation is actually used.
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "selenium is required to launch the browser. Install it (e.g. `pip install selenium`)."
        ) from e

    options = Options()
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=options)

