# asset_update_api.py — LEVEL_5

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1.session_manager import (
    open_asset_updater,
    wait_for_post_auth_ready,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_4.loop_runner import (
    run_asset_update_loop,
)


def run_asset_update(page: Page, url: str, dataset) -> None:
    """
    Main entrypoint for asset updater automation.
    
    Flow:
    1. Navigate to login page
    2. Wait for manual authentication (user completes login + Duo)
    3. Wait for post-auth page to be ready
    4. Run the automation loop
    """
    
    # Step 1: Navigate to login
    open_asset_updater(page, url)
    
    print("\n" + "="*60)
    print("MANUAL AUTHENTICATION REQUIRED")
    print("="*60)
    print("Please complete the following in the browser window:")
    print("  1. Click 'Accept' on the terms page")
    print("  2. Log in with your UNT credentials")
    print("  3. Complete Duo Mobile MFA")
    print("  4. Wait for the asset updater page to fully load")
    print("\nThe automation will resume automatically...")
    print("="*60 + "\n")
    
    # Step 2: Wait for post-authentication page to be ready
    wait_for_post_auth_ready(page)
    
    # Step 3: Run automation loop
    run_asset_update_loop(page, dataset)