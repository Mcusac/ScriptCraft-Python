# ============================================================
# row_executor.py — LEVEL_5
# ============================================================

from typing import Any
from typing import Dict

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    EMPLOYEE_ID_ROW_KEYS,
    LOCATION_CODE_ROW_KEYS,
    TAG_NUMBER_ROW_KEYS,
    TAG_PAD_WIDTH,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    optional_employee_id_from_row,
    optional_location_code_from_row,
    tag_number_from_row,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    execute_asset_post_update_step,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    execute_asset_search_step,
    execute_asset_update_step,
)


def execute_asset_update_row(
    page: Page,
    row: Dict[str, Any],
    *,
    clear_asset_id: bool = False,
) -> None:
    """
    DAG-style row execution:
    SEARCH → UPDATE → SUBMIT
    """

    tag_number = tag_number_from_row(
        row,
        TAG_NUMBER_ROW_KEYS,
        pad_width=TAG_PAD_WIDTH,
    )

    execute_asset_search_step(
        page,
        tag_number,
        clear_asset_id=clear_asset_id,
    )

    execute_asset_update_step(
        page,
        location_code=optional_location_code_from_row(row, LOCATION_CODE_ROW_KEYS),
        employee_id=optional_employee_id_from_row(row, EMPLOYEE_ID_ROW_KEYS),
    )

    execute_asset_post_update_step(page)
