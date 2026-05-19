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

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    constants as c,
)


def page_contains_selector(
    page: Page,
    selector: str,
) -> bool:
    """
    Search top page and all frames.
    """

    try:

        if page.query_selector(selector) is not None:
            return True

        for frame in page.frames:

            try:

                if frame.query_selector(selector) is not None:
                    return True

            except Exception:
                continue

        return False

    except Exception:
        return False


def is_login_page(page: Page) -> bool:

    return (
        page_contains_selector(
            page,
            c.LOGIN_FORM_USERID_SELECTOR,
        )
        or page_contains_selector(
            page,
            c.LOGIN_FORM_PASSWORD_SELECTOR,
        )
    )


def is_mfa_page(page: Page) -> bool:
    """
    Detect active Duo MFA flow.

    Duo in UNT SSO is a full-page redirect, not an embedded iframe.
    """

    try:

        current_url = page.url.lower()

        if c.DUO_URL_KEYWORD in current_url:
            return True

        return False

    except Exception:
        return False


def is_authenticated_page(page: Page) -> bool:

    has_business_unit = page_contains_selector(
        page,
        c.BUSINESS_UNIT_INPUT_SELECTOR,
    )

    has_search_button = page_contains_selector(
        page,
        c.SEARCH_BUTTON_SELECTOR,
    )

    return (
        has_business_unit
        and has_search_button
    )


def get_page_state(page: Page) -> str:

    try:

        if is_login_page(page):
            return c.STATE_LOGIN_PAGE

        if is_mfa_page(page):
            return c.STATE_MFA_PAGE

        if is_authenticated_page(page):
            return c.STATE_AUTHENTICATED

        return c.STATE_UNKNOWN

    except Exception:
        return c.STATE_UNKNOWN
