# orchestration_runner.py — LEVEL_0
import pandas as pd

from pathlib import Path

from playwright.sync_api import sync_playwright

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_7.runner import (
    run as run_reconciliation,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0.constants import (
    ASSET_UPDATER_URL,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_5.asset_update_api import (
    run_asset_update,
)


def run_asset_management_workflow(
    asset_csv: Path,
    form_csv: Path,
    output_dir: Path,
    debug: bool = False,
) -> None:
    """
    Runs full reconciliation + updater workflow.
    """

    # ---------------------------------------------------------
    # reconciliation
    # ---------------------------------------------------------

    run_reconciliation(
        asset_csv=asset_csv,
        form_csv=form_csv,
        output_dir=output_dir,
        debug=debug,
    )

    # ---------------------------------------------------------
    # load updater dataset
    # ---------------------------------------------------------

    dataset_path = (
        output_dir / "asset_update_dataset.csv"
    )

    dataset = pd.read_csv(
        dataset_path,
        dtype=str,
    ).to_dict(orient="records")

    # ---------------------------------------------------------
    # updater automation
    # ---------------------------------------------------------

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
        )

        page = browser.new_page()

        run_asset_update(
            page=page,
            url=ASSET_UPDATER_URL,
            dataset=dataset,
        )

        browser.close()