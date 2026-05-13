# run_asset_update_test.py

import pandas as pd
from playwright.sync_api import sync_playwright

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_5.asset_update_api import (
    run_asset_update,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0.constants import (
    ASSET_UPDATER_URL,
)


def load_test_data():
    """
    Loads only first 2 rows from both CSVs and merges them.
    """

    location_df = pd.read_csv(
        "workspace/input/location_changes_test.csv"
    ).head(2)

    custodian_df = pd.read_csv(
        "workspace/input/custodian_changes_test.csv"
    ).head(2)

    # ASSUMPTION: shared key is tag
    dataset = location_df.merge(
        custodian_df,
        on="tag",
        how="inner"
    )

    return dataset.to_dict("records")


def main():
    dataset = load_test_data()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        run_asset_update(page, ASSET_UPDATER_URL, dataset)

        browser.close()


if __name__ == "__main__":
    main()