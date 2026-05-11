# loop_runner.py — LEVEL_4

from typing import List, Dict, Any
from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1.session_manager import (
    set_business_unit,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_3.row_executor import (
    execute_asset_update_row,
)


def run_asset_update_loop(page: Page, dataset: List[Dict[str, Any]]) -> None:
    """
    Controls iteration + failure isolation.
    """

    set_business_unit(page)

    for idx, row in enumerate(dataset):

        try:
            execute_asset_update_row(page, row)

        except Exception as e:
            print(
                f"[ERROR] Row {idx} failed "
                f"(Tag={row.get('Tag Number')}): {e}"
            )
            continue