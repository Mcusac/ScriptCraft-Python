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

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
    constants as c,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    load_credentials,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    assist_login_page,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    get_page_state,
    is_authenticated_page,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_2 import (
    log_page_diagnostics,
)

POST_AUTH_SETTLE_MS = 1_500


def open_asset_updater(
    page: Page,
    url: str,
) -> None:

    ba.navigate(page, url)
    ba.wait_for_page_load(page)


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
    timeout_ms: int = c.POST_AUTH_TIMEOUT_MS,
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

        if current_state == c.STATE_AUTHENTICATED:

            if not is_authenticated_page(page):
                ba.safe_wait(
                    page,
                    c.STATE_CHECK_INTERVAL_MS,
                )
                continue

            ba.safe_wait(page, POST_AUTH_SETTLE_MS)

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

        ba.safe_wait(
            page,
            c.STATE_CHECK_INTERVAL_MS,
        )
