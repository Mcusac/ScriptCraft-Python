# ============================================================
# row_executor.py — LEVEL_3
# ============================================================

from typing import Any
from typing import Dict

from playwright.sync_api import Page


from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    LOCATION_CODE_ROW_KEYS,
    EMPLOYEE_ID_ROW_KEYS,
    TAG_NUMBER_ROW_KEYS,
    TAG_PAD_WIDTH,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    execute_asset_post_update_step,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    execute_asset_search_step,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    UpdateKind,
    optional_location_code_from_row,
    optional_employee_id_from_row,
    location_code_from_row,
    employee_id_from_row,
    classify_update_row,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    execute_asset_update_step,
)


def tag_number_from_row(row: Dict[str, Any]) -> str:
    return tag_number_from_row(
        row,
        TAG_NUMBER_ROW_KEYS,
        pad_width=TAG_PAD_WIDTH,
    )


def optional_location_code_from_row(row: Dict[str, Any]) -> str | None:
    return optional_location_code_from_row(
        row,
        LOCATION_CODE_ROW_KEYS,
    )


def optional_employee_id_from_row(row: Dict[str, Any]) -> str | None:
    return optional_employee_id_from_row(
        row,
        EMPLOYEE_ID_ROW_KEYS,
    )


def location_code_from_row(row: Dict[str, Any]) -> str:
    return location_code_from_row(
        row,
        LOCATION_CODE_ROW_KEYS,
    )


def employee_id_from_row(row: Dict[str, Any]) -> str:
    return employee_id_from_row(
        row,
        EMPLOYEE_ID_ROW_KEYS,
    )


def classify_update_row(row: Dict[str, Any]) -> UpdateKind:
    return classify_update_row(
        row,
        location_keys=LOCATION_CODE_ROW_KEYS,
        employee_keys=EMPLOYEE_ID_ROW_KEYS,
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

    tag_number = tag_number_from_row(row)

    execute_asset_search_step(
        page,
        tag_number,
        clear_asset_id=clear_asset_id,
    )

    execute_asset_update_step(
        page,
        location_code=optional_location_code_from_row(row),
        employee_id=optional_employee_id_from_row(row),
    )

    execute_asset_post_update_step(page)
