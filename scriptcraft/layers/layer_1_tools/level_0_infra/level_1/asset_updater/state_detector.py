# ============================================================
# state_detector.py — LEVEL_1
#
# PURPOSE:
# - DOM-based authentication state detection
# - Pure page classification logic
#
# DESIGN:
# - No orchestration
# - No waits
# - No logging
# - No navigation
# ============================================================

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    selector_exists,
    DUO_URL_KEYWORD,
    LOGIN_FORM_USERID_SELECTOR,
    LOGIN_FORM_PASSWORD_SELECTOR,
    BUSINESS_UNIT_INPUT_SELECTOR,
    SEARCH_BUTTON_SELECTOR,
    STATE_LOGIN_PAGE,
    STATE_MFA_PAGE,
    STATE_AUTHENTICATED,
    STATE_UNKNOWN,
)


def page_contains_selector(
    page: Page,
    selector: str,
) -> bool:
    """Search top page and all frames via shared browser primitive."""
    return selector_exists(page, selector)


def is_login_page(page: Page) -> bool:

    return (
        page_contains_selector(
            page,
            LOGIN_FORM_USERID_SELECTOR,
        )
        or page_contains_selector(
            page,
            LOGIN_FORM_PASSWORD_SELECTOR,
        )
    )


def is_mfa_page(page: Page) -> bool:
    """
    Detect active Duo MFA flow.

    Duo in UNT SSO is a full-page redirect, not an embedded iframe.
    """

    try:

        current_url = page.url.lower()

        if DUO_URL_KEYWORD in current_url:
            return True

        return False

    except Exception:
        return False


def is_authenticated_page(page: Page) -> bool:

    has_business_unit = page_contains_selector(
        page,
        BUSINESS_UNIT_INPUT_SELECTOR,
    )

    has_search_button = page_contains_selector(
        page,
        SEARCH_BUTTON_SELECTOR,
    )

    return (
        has_business_unit
        and has_search_button
    )


def get_page_state(page: Page) -> str:

    try:

        if is_login_page(page):
            return STATE_LOGIN_PAGE

        if is_mfa_page(page):
            return STATE_MFA_PAGE

        if is_authenticated_page(page):
            return STATE_AUTHENTICATED

        return STATE_UNKNOWN

    except Exception:
        return STATE_UNKNOWN
