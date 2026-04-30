"""
Login-related Selenium actions for `rhq_form_autofiller`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_tools.level_1_impl.level_0.rhq.credentials_io import load_credentials


def try_click_initial_login_button(driver: Any, *, timeout_s: int = 10) -> bool:
    """
    Click the initial 'Login' button if present to reveal the login form.
    Returns True if clicked, False otherwise.
    """
    try:
        login_btn = WebDriverWait(driver, timeout_s).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
        )
        login_btn.click()
        log_and_print("🔐 Login button clicked - login form should now be visible.")
        return True
    except Exception as e:
        log_and_print(f"⚠️ Could not click initial Login button: {e}", level="warning")
        return False


def attempt_automatic_login(
    driver: Any,
    *,
    logger: Optional[Any] = None,
    credentials_file: Optional[Path] = None,
) -> bool:
    """
    Attempt automatic login if credentials are available.

    Returns True if login was attempted, False otherwise.
    """
    credentials_file = credentials_file or (Path(__file__).parent / "credentials.txt")
    username, password = load_credentials(credentials_file)

    if not username or not password:
        log_msg = "ℹ️ No credentials found in credentials.txt, manual login required"
        if logger:
            logger.info(log_msg)
        else:
            log_and_print(log_msg)
        return False

    try:
        log_msg = f"🔐 Attempting automatic login for user: {username}"
        if logger:
            logger.info(log_msg)
        else:
            log_and_print(log_msg)

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "input[type='email'], input[type='text'], input[name='username'], input[name='email']",
                )
            )
        )
        username_field.clear()
        username_field.send_keys(username)

        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.clear()
        password_field.send_keys(password)

        login_button = driver.find_element(
            By.XPATH,
            "//button[contains(text(), 'Login') or contains(text(), 'Sign In') or contains(text(), 'Log In')]",
        )
        login_button.click()

        log_msg = "✅ Automatic login credentials entered, waiting for authentication..."
        if logger:
            logger.info(log_msg)
        else:
            log_and_print(log_msg)

        return True

    except Exception as e:
        log_msg = f"⚠️ Automatic login failed: {e}, falling back to manual login"
        if logger:
            logger.warning(log_msg)
        else:
            log_and_print(log_msg, level="warning")
        return False

