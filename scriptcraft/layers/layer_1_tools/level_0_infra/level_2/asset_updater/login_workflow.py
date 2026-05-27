# ============================================================
# login_workflow.py —
#
# PURPOSE:
# - UNT login page assist (terms, credentials, sign in)
# ============================================================

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    LOGIN_FORM_USERID_SELECTOR,
    LOGIN_FORM_PASSWORD_SELECTOR,
    LOGIN_SUBMIT_BUTTON_SELECTOR,
    TERMS_ACCEPT_BUTTON_SELECTOR,
    TERMS_MODAL_APPEAR_DELAY_MS,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    click,
    click_button_if_present,
    fill_input,
)


def assist_login_page(
    page: Page,
    username: str,
    password: str,
) -> None:
    """
    Accept terms modal, fill EUID/password, and submit login form.
    Duo MFA remains manual.
    """

    page.wait_for_timeout(TERMS_MODAL_APPEAR_DELAY_MS)
    click_button_if_present(page, TERMS_ACCEPT_BUTTON_SELECTOR, timeout_ms=10_000)

    fill_input(
        page,
        LOGIN_FORM_USERID_SELECTOR,
        username,
    )

    fill_input(
        page,
        LOGIN_FORM_PASSWORD_SELECTOR,
        password,
    )

    click(page, LOGIN_SUBMIT_BUTTON_SELECTOR)
    page.wait_for_load_state("domcontentloaded")

