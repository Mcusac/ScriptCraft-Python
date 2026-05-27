# ============================================================
# asset_update_api.py — LEVEL_5
# ============================================================

from typing import Any
from typing import Dict
from typing import List

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    open_asset_updater,
    wait_for_post_auth_ready,
    assist_login_if_configured,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    run_asset_update_loop,
)


def _print_auth_instructions(login_assisted: bool) -> None:

    print("\n" + "=" * 60)

    if login_assisted:
        print("LOGIN ASSIST ACTIVE")
        print("=" * 60)
        print("Automated: terms accept, EUID/password, Sign in")
        print("Manual: complete Duo MFA when prompted")
        print("Automation resumes on the asset page.")
    else:
        print("MANUAL AUTHENTICATION REQUIRED")
        print("=" * 60)
        print("Complete the following steps:")
        print("  1. Accept terms")
        print("  2. Login with UNT credentials")
        print("  3. Complete Duo MFA")
        print("  4. Wait for asset page to load")
        print("\nAutomation will resume automatically.")

    print("=" * 60 + "\n")


def run_asset_update(
    page: Page,
    url: str,
    dataset: List[Dict[str, Any]],
) -> None:
    """
    Main orchestration entrypoint for asset updater.
    """

    open_asset_updater(
        page,
        url,
    )

    login_assisted = assist_login_if_configured(page)

    _print_auth_instructions(login_assisted)

    wait_for_post_auth_ready(page)

    run_asset_update_loop(
        page,
        dataset,
    )
