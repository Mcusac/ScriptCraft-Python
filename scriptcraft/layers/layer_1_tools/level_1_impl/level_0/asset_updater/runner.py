# ============================================================
# runner.py — asset updater orchestration (impl L0)
# ============================================================

from typing import Any, Dict, List

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    EMPLOYEE_ID_ROW_KEYS,
    LOCATION_CODE_ROW_KEYS,
    TAG_NUMBER_ROW_KEYS,
    TAG_PAD_WIDTH,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    classify_update_row,
    tag_number_from_row,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    assist_login_if_configured,
    open_asset_updater,
    wait_for_post_auth_ready,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    recover_to_asset_search,
    set_business_unit,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_5 import (
    execute_asset_update_row,
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


def run_asset_update_loop(
    page: Page,
    dataset: List[Dict[str, Any]],
) -> None:
    """Iterate dataset rows with failure isolation and recovery."""
    set_business_unit(page)

    total_rows = len(dataset)

    print(f"\nStarting asset update loop ({total_rows} rows)...")

    for idx, row in enumerate(dataset, start=1):
        try:
            tag_number = tag_number_from_row(
                row,
                TAG_NUMBER_ROW_KEYS,
                pad_width=TAG_PAD_WIDTH,
            )
        except KeyError:
            tag_number = "UNKNOWN"

        try:
            update_kind = classify_update_row(
                row,
                location_keys=LOCATION_CODE_ROW_KEYS,
                employee_keys=EMPLOYEE_ID_ROW_KEYS,
            )
        except Exception:
            update_kind = "unknown"

        print(f"\n[{idx}/{total_rows}] Processing tag: {tag_number} ({update_kind})")

        try:
            execute_asset_update_row(
                page,
                row,
                clear_asset_id=(idx > 1),
            )
            print(f"[SUCCESS] Tag {tag_number}")
        except Exception as e:
            print(f"[ERROR] Row failed (Tag={tag_number}): {e}")

            try:
                if recover_to_asset_search(page):
                    set_business_unit(page)
                    print(f"[RECOVERED] Ready for next tag after failure on {tag_number}")
                else:
                    print("[WARN] Recovery incomplete; next row may fail")
            except Exception as recovery_error:
                print(f"[WARN] Recovery failed: {recovery_error}")

            continue


def run_asset_update(
    page: Page,
    url: str,
    dataset: List[Dict[str, Any]],
) -> None:
    """Open asset updater, authenticate, and run the update loop."""
    open_asset_updater(page, url)

    login_assisted = assist_login_if_configured(page)
    _print_auth_instructions(login_assisted)

    wait_for_post_auth_ready(page)
    run_asset_update_loop(page, dataset)
