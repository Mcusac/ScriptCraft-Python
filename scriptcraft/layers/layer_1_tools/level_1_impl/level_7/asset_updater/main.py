# ============================================================
# run_asset_update_test.py
# ============================================================

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    ASSET_URL,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_3.asset_updater import (
    load_updater_dataset,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_5 import (
    run_asset_update,
)

LOCATION_CSV = Path(
    "workspace/input/location_changes.csv"
)

CUSTODIAN_CSV = Path(
    "workspace/input/custodian_changes.csv"
)


def main():

    dataset = load_updater_dataset(
        LOCATION_CSV,
        CUSTODIAN_CSV,
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
        )

        page = browser.new_page()

        try:

            run_asset_update(
                page=page,
                url=ASSET_URL,
                dataset=dataset,
            )

            print(
                "\n[OK] Asset update automation "
                "completed successfully"
            )

        except Exception as e:

            print(
                f"\n[FAILED] Automation failed: {e}"
            )

            print(
                "Browser window will close "
                "in 5 seconds..."
            )

            time.sleep(5)

        finally:

            browser.close()


if __name__ == "__main__":
    main()
