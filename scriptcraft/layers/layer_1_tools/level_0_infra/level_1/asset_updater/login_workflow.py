# ============================================================
# login_workflow.py —
#
# PURPOSE:
# - UNT login page assist (terms, credentials, sign in)
# ============================================================

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    click,
    fill_input,
    wait_for_page_load,
    click_terms_accept_if_present,
    LOGIN_FORM_USERID_SELECTOR,
    LOGIN_FORM_PASSWORD_SELECTOR,
    LOGIN_SUBMIT_BUTTON_SELECTOR,
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

    click_terms_accept_if_present(page)

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
    wait_for_page_load(page)
