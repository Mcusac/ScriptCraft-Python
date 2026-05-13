# ============================================================
# row_executor.py — LEVEL_3
# ============================================================

from typing import Dict, Any
from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1.asset_search_step import (
    execute_asset_search_step,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1.asset_post_update_step import (
    execute_asset_post_update_step,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_2.asset_update_step import (
    execute_asset_update_step,
)

def execute_asset_update_row(page: Page, row: Dict[str, Any]) -> None:
    """
    DAG-style row execution:
    SEARCH → UPDATE → SUBMIT
    """

    execute_asset_search_step(page, row["Tag Number"])

    execute_asset_update_step(
        page,
        location_code=row["location_norm_forms"],
        employee_id=row["user_norm_forms"],
    )

    execute_asset_post_update_step(page)