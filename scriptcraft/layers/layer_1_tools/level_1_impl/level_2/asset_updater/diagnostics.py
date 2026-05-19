# ============================================================
# diagnostics.py — LEVEL_2
#
# PURPOSE:
# - Page diagnostics and debugging helpers
#
# DESIGN:
# - Debugging only
# - No orchestration
# ============================================================

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
    constants as c,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    get_page_state,
    page_contains_selector,
)


def _log_frame_summary(page: Page) -> None:

    frames = page.frames

    print(f"\nFrames ({len(frames)}):")

    for idx, frame in enumerate(frames):

        try:
            frame_url = frame.url
        except Exception:
            frame_url = "(unavailable)"

        print(f"  [{idx}] {frame_url}")


def log_page_diagnostics(
    page: Page,
    label: str = "",
) -> None:

    print(f"\n[DIAGNOSTICS] {label}")
    print("─" * 60)

    print(f"URL: {ba.get_page_url(page)}")
    print(f"Title: {ba.get_page_title(page)}")

    state = get_page_state(page)

    print(f"Detected State: {state}")

    _log_frame_summary(page)

    all_inputs = page.query_selector_all(
        c.DIAGNOSTIC_ALL_TEXT_INPUTS
    )

    print(
        f"\nText/Password inputs on top document: "
        f"{len(all_inputs)}"
    )

    for idx, inp in enumerate(all_inputs[:10]):

        inp_id = inp.get_attribute("id") or "(no id)"
        inp_name = inp.get_attribute("name") or "(no name)"
        inp_type = inp.get_attribute("type") or "text"

        print(
            f"  [{idx}] "
            f"type={inp_type}, "
            f"id={inp_id}, "
            f"name={inp_name}"
        )

    print("\nKey element checks (page + frames):")

    login_exists = page_contains_selector(
        page,
        c.LOGIN_FORM_USERID_SELECTOR,
    )

    password_exists = page_contains_selector(
        page,
        c.LOGIN_FORM_PASSWORD_SELECTOR,
    )

    business_unit_exists = page_contains_selector(
        page,
        c.BUSINESS_UNIT_INPUT_SELECTOR,
    )

    search_button_exists = page_contains_selector(
        page,
        c.SEARCH_BUTTON_SELECTOR,
    )

    print(f"  Login form: {login_exists}")
    print(f"  Password input: {password_exists}")
    print(f"  Business unit: {business_unit_exists}")
    print(f"  Search button: {search_button_exists}")

    print("─" * 60 + "\n")
