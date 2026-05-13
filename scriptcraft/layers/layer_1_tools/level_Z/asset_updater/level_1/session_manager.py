# ============================================================
# session_manager.py — LEVEL_1
# ============================================================

import time

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    browser_actions as ba,
    constants as c,
)


def open_asset_updater(page: Page, url: str) -> None:
    """
    Navigates to asset updater system.
    """
    ba.navigate(page, url)
    ba.wait_for_page_load(page)


def wait_for_post_auth_ready(page: Page, timeout_ms: int = 60_000) -> None:
    """
    Orchestrates post-authentication readiness checks.
    """

    print("[POST-AUTH] Waiting for asset updater page to be ready...")

    wait_for_asset_updater_url(
        page,
        timeout_ms,
    )

    wait_for_asset_updater_page_load(
        page,
        timeout_ms,
    )

    wait_for_business_unit_field(
        page,
        timeout_ms,
    )


def wait_for_asset_updater_url(
    page: Page,
    timeout_ms: int,
) -> None:
    """
    Waits until browser reaches the real asset updater page.
    """

    start_time = time.time()
    max_wait = timeout_ms / 1000.0

    while time.time() - start_time < max_wait:
        current_url = ba.get_page_url(page)

        if "GBAM_MANAGE_ASSETS" in current_url:
            print(f"[POST-AUTH] ✓ Correct page URL detected: {current_url}")
            return

        ba.safe_wait(page, 500)

    print("[POST-AUTH] ✗ Timeout waiting for asset updater URL")
    ba.log_page_state(page, "[POST-AUTH]")

    raise TimeoutError(
        "Did not reach asset updater page after authentication.\n"
        f"Current URL: {ba.get_page_url(page)}"
    )


def wait_for_asset_updater_page_load(
    page: Page,
    timeout_ms: int,
) -> None:
    """
    Waits for asset updater page load completion.
    """

    print("[POST-AUTH] Waiting for page load...")

    ba.wait_for_page_load(
        page,
        timeout_ms=timeout_ms,
    )

    print("[POST-AUTH] ✓ Page load complete")


def wait_for_business_unit_field(
    page: Page,
    timeout_ms: int,
) -> None:
    """
    Waits for business unit field readiness.
    """

    print("[POST-AUTH] Waiting for business unit field to be ready...")

    try:
        if not ba.selector_exists(
            page,
            c.BUSINESS_UNIT_INPUT_SELECTOR,
        ):
            print(
                f"[POST-AUTH] ✗ Selector does not exist: "
                f"{c.BUSINESS_UNIT_INPUT_SELECTOR}"
            )

            ba.log_page_state(page, "[POST-AUTH]")

            print("[POST-AUTH] Attempting to find alternative selectors...")

            try:
                all_inputs = page.query_selector_all(
                    "input[type='text']"
                )

                print(
                    f"[POST-AUTH] Found {len(all_inputs)} text input fields on page"
                )

                for idx, inp in enumerate(all_inputs[:5]):
                    inp_id = inp.get_attribute("id")
                    inp_name = inp.get_attribute("name")

                    print(
                        f"[POST-AUTH]   Input {idx}: "
                        f"id={inp_id}, "
                        f"name={inp_name}"
                    )

            except Exception as e:
                print(
                    f"[POST-AUTH] Could not enumerate inputs: {e}"
                )

            raise RuntimeError(
                "Business unit selector not found:\n"
                f"{c.BUSINESS_UNIT_INPUT_SELECTOR}"
            )

        ba.wait_for_selector_with_diagnostics(
            page,
            c.BUSINESS_UNIT_INPUT_SELECTOR,
            timeout_ms=timeout_ms,
        )

        print("[POST-AUTH] ✓ Business unit field is ready")

    except Exception as e:
        print(
            f"[POST-AUTH] ✗ Failed to locate business unit field: {e}"
        )
        raise


def set_business_unit(page: Page) -> None:
    """
    Sets static business unit.
    """

    ba.fill_input(
        page,
        c.BUSINESS_UNIT_INPUT_SELECTOR,
        c.BUSINESS_UNIT_VALUE,
    )

    ba.safe_wait(page, 1000)