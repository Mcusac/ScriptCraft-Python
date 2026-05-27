# ============================================================
# session_manager.py — LEVEL_3
#
# PURPOSE:
# - Authentication orchestration
# - Post-auth readiness waiting
# - Asset updater initialization
#
# DESIGN:
# - Orchestration only
# - No DOM interrogation (delegates to state_detector)
# ============================================================

import time

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    navigate,
    safe_wait,
    wait_for_page_load,
    POST_AUTH_TIMEOUT_MS,
    STATE_CHECK_INTERVAL_MS,
    STATE_AUTHENTICATED,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    get_page_state,
    is_authenticated_page,
    load_credentials,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    assist_login_page,
    log_page_diagnostics,
)

POST_AUTH_SETTLE_MS = 1_500


def open_asset_updater(
    page: Page,
    url: str,
) -> None:
    navigate(page, url)
    wait_for_page_load(page)


def assist_login_if_configured(page: Page) -> bool:
    """
    When credentials.py is present, accept terms and submit login.
    Returns True if login assist ran.
    """

    creds = load_credentials()

    if creds is None:
        print(
            "[LOGIN] No credentials.py — "
            "complete login manually."
        )
        return False

    username, password = creds

    print(
        "[LOGIN] Assisting: terms + "
        "credential fill + Sign in..."
    )

    assist_login_page(page, username, password)

    return True


def wait_for_post_auth_ready(
    page: Page,
    timeout_ms: int = POST_AUTH_TIMEOUT_MS,
) -> None:

    print("\nWaiting for authentication completion...")

    start_time = time.time()
    last_state = None

    while True:

        current_state = get_page_state(page)

        if current_state != last_state:

            elapsed = time.time() - start_time

            print(
                f"[{elapsed:.1f}s] "
                f"State: {current_state}"
            )

            last_state = current_state

        if current_state == STATE_AUTHENTICATED:

            if not is_authenticated_page(page):
                safe_wait(
                    page,
                    STATE_CHECK_INTERVAL_MS,
                )
                continue

            safe_wait(page, POST_AUTH_SETTLE_MS)

            elapsed = time.time() - start_time

            print(
                f"Authenticated after "
                f"{elapsed:.1f}s"
            )

            return

        elapsed_ms = (time.time() - start_time) * 1000

        if elapsed_ms > timeout_ms:

            log_page_diagnostics(
                page,
                "AUTH TIMEOUT",
            )

            raise TimeoutError(
                "Authentication did not complete within timeout.\n"
                f"Last state: {last_state}"
            )

        safe_wait(
            page,
            STATE_CHECK_INTERVAL_MS,
        )

