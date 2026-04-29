"""
Orchestration flow for `rhq_form_autofiller`.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_pypi.level_1_impl.level_0.rhq.waits import wait_until_not_on_login
from layers.layer_1_pypi.level_1_impl.level_1.rhq_login_actions import try_click_initial_login_button

def handle_login(
    driver: Any,
    *,
    data: Dict[str, Any],
    config: Any,
    logger: Optional[Any],
    form_wait_time: int,
    browser_timeout: int,
    attempt_automatic_login_func,
) -> None:
    """Navigate to first record and complete login (auto if possible)."""
    first_med_id = next(iter(data))
    url = config.tools["rhq_form_autofiller"]["url_template"].format(med_id=first_med_id)

    log_and_print("🔑 Attempting automatic login")
    driver.get(url)
    driver.refresh()
    log_and_print("🔄 Refreshed to ensure login screen.")

    time.sleep(form_wait_time)
    log_and_print(f"⏱️ Waiting {form_wait_time} seconds for page to fully load...")

    try_click_initial_login_button(driver, timeout_s=10)
    time.sleep(2)

    login_attempted = attempt_automatic_login_func(driver, logger=logger)

    if not login_attempted:
        log_and_print("ℹ️ Automatic login not attempted - manual login required.")
    else:
        log_and_print("🤖 Automatic login attempted - waiting for authentication...")

    wait_until_not_on_login(driver, timeout_s=browser_timeout)
    log_and_print("✅ Login confirmed. Starting data entry...")
    time.sleep(5)


def submit_form(driver: Any, med_id: str) -> None:
    """Click Submit/Save and wait briefly."""
    try:
        log_and_print(f"💾 Submitting form for {med_id}...")
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Save')]")
            )
        )
        submit_btn.click()
        time.sleep(3)
        log_and_print(f"✅ Form submitted for {med_id}")
    except Exception as e:
        log_and_print(f"⚠️ Could not submit form for {med_id}: {e}", level="warning")

