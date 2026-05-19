# ============================================================
# login_workflow.py — LEVEL_1
#
# PURPOSE:
# - UNT login page assist (terms, credentials, sign in)
# ============================================================

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
    constants as c,
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

    ba.click_terms_accept_if_present(page)

    ba.fill_input(
        page,
        c.LOGIN_FORM_USERID_SELECTOR,
        username,
    )

    ba.fill_input(
        page,
        c.LOGIN_FORM_PASSWORD_SELECTOR,
        password,
    )

    ba.click(page, c.LOGIN_SUBMIT_BUTTON_SELECTOR)
    ba.wait_for_page_load(page)
